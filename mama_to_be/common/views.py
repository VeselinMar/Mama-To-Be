import logging
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views import View
from django.http import Http404, JsonResponse
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.core.cache import cache
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector
)
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit
from .utility import process_image_to_webp
from ..articles.models import Article
from ..food.models import Recipe
from .forms import ContactForm
from django.utils.translation import get_language
from django.utils.html import escape
from concurrent.futures import ThreadPoolExecutor
import traceback
import uuid

# Create your views here.

logger = logging.getLogger("contact")

class HomeView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        language = get_language()

        context["latest_article"] = (
            Article.objects.translated(language_code=language)
            .select_related("author")
            .order_by("-created_at")
            .first()
        )

        context["latest_recipe"] = (
            Recipe.objects.translated(language_code=language)
            .select_related("author")
            .prefetch_related(
                "tags",
                "ingredients",
            )            
            .order_by("-created_at")
            .first()
        )

        return context

class PrivacyView(TemplateView):
    template_name = 'common/footer_related/privacy.html'

class ImpressumView(TemplateView):
    template_name = 'common/footer_related/impressum.html'


class AboutView(TemplateView):
    template_name = 'common/footer_related/about.html'

@require_POST
def upload_image(request):
    print("METHOD:", request.method)

    uploaded_file = request.FILES.get("file")
    print("FILES:", request.FILES)
    print("POST:", request.POST)
    print("CONTENT TYPE:", request.content_type)
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        content_file = process_image_to_webp(uploaded_file)
        path = default_storage.save(content_file.name, content_file)
        url = default_storage.url(path)

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"location": url})

def lang_to_pg_config(lang_code):
    mapping = {
        'en': 'english', 'de': 'german',
    }
    base = lang_code.split('-')[0].lower()
    return mapping.get(base, 'simple')

@ratelimit(key='ip', rate='30/m', method='GET', block=False)
def search_view(request):
    q = request.GET.get('q', '').strip()
    lang = request.LANGUAGE_CODE
    config = lang_to_pg_config(lang)

    results = []

    if getattr(request, "limited", False):
        return render(request, "common/search_results.html", {
            "results": [],
            "query": q,
            "error": "Too many requests. Please slow down."
        })

    if q and len(q) <= 100:
        query = SearchQuery(q, config=config, search_type='websearch')

        vector_article = (
            SearchVector('translations__title', weight='A', config=config) +
            SearchVector('translations__content', weight='B', config=config)
        )
        vector_recipe = (
            SearchVector('translations__name', weight='A', config=config) +
            SearchVector('translations__text', weight='B', config=config)
        )

        article_qs = (
            Article.objects.language(lang)
            .filter(is_published=True)
            .annotate(rank=SearchRank(vector_article, query))
            .filter(rank__gt=0)
            .order_by('-rank')[:10]
        )

        recipe_qs = (
            Recipe.objects.language(lang)
            .annotate(rank=SearchRank(vector_recipe, query))
            .filter(rank__gt=0)
            .order_by('-rank')[:10]
        )

        with ThreadPoolExecutor(max_workers=2) as executor:
            future_articles = executor.submit(list, article_qs)
            future_recipes = executor.submit(list, recipe_qs)
            articles = future_articles.result()
            recipes = future_recipes.result()

        results = (
            [{'type': 'article', 'obj': a, 'rank': a.rank} for a in articles] +
            [{'type': 'recipe',  'obj': r, 'rank': r.rank} for r in recipes]
        )
        results.sort(key=lambda x: x['rank'], reverse=True)

    return render(request, 'common/search_results.html', {'results': results, 'query': q})

@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def contact_view(request):

    ip = request.META.get("REMOTE_ADDR")

    if getattr(request, 'limited', False):
        logger.warning("RATE_LIMIT_TRIGGERED ip=%s", ip)
        messages.error(request, "Too many requests. Please wait a moment.")
        return redirect("contact")

    if request.method == "POST":

        form = ContactForm(request.POST)
        token = request.POST.get("submission_token")

        # 1. Validate token (single-use protection)
        if not token or not cache.get(token):
            logger.warning("INVALID_OR_EXPIRED_TOKEN ip=%s token=%s", ip, token)
            messages.error(request, "This form was already submitted or expired.")
            return redirect("contact")

        if form.is_valid():

            # -----------------------------
            # CLEAN INPUT
            # -----------------------------
            name = form.cleaned_data["name"].strip().replace("\n", " ")
            email_addr = form.cleaned_data["email"].strip()
            message_text = form.cleaned_data["message"].strip()

            safe_name = escape(name)
            safe_email = escape(email_addr)
            safe_message = escape(message_text)

            subject = f"New contact form message from {name}"

            # -----------------------------
            # EMAIL CONTENT (TEXT)
            # -----------------------------
            text_content = f"""
New Contact Message

Name: {name}
Email: {email_addr}

Message:
{message_text}
"""

            # -----------------------------
            # EMAIL CONTENT (HTML)
            # -----------------------------
            html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background:#f9f9f9; padding:20px;">

    <div style="max-width:600px; margin:auto; background:#ffffff; padding:20px; border-radius:8px;">

      <h2 style="margin-top:0;">New Contact Message</h2>

      <p><strong>Name:</strong> {safe_name}</p>
      <p><strong>Email:</strong> {safe_email}</p>

      <hr style="border:none; border-top:1px solid #eee;" />

      <h3>Message</h3>
      <div style="background:#f4f4f4; padding:12px; border-radius:6px; white-space:pre-wrap;">
        {safe_message}
      </div>

    </div>

  </body>
</html>
"""

            try:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECEIVER_EMAIL],
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # 2. Consume token ONLY after successful send
                cache.delete(token)

                logger.info(
                    "CONTACT_EMAIL_SENT ip=%s email_domain=%s",
                    ip,
                    email_addr.split("@")[-1] if email_addr else None
                )

                messages.success(request, "Message sent successfully")
                return redirect("contact")

            except Exception:
                logger.exception(
                    "CONTACT_EMAIL_FAILED ip=%s email=%s",
                    ip,
                    email_addr,
                )

                messages.error(request, "Failed to send message. Please try again.")
                return render(request, "common/footer_related/contact.html", {
                    "form": form,
                    "submission_token": token,
                })

        else:
            logger.warning("CONTACT_FORM_INVALID ip=%s", ip)

            messages.error(request, "Please correct the errors below.")
            return render(request, "common/footer_related/contact.html", {
                "form": form,
                "submission_token": token,
            })

    # GET → create token
    submission_token = str(uuid.uuid4())
    cache.set(submission_token, True, timeout=300)

    return render(request, "common/footer_related/contact.html", {
        "form": ContactForm(),
        "submission_token": submission_token,
    })