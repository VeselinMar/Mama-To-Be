from django.views.generic import TemplateView
from django.views.decorators.http import require_POST


# Create your views here.

class HomeView(TemplateView):
    template_name = 'common/home.html'

class PrivacyView(TemplateView):
    template_name = 'common/footer_related/privacy.html'

class ImpressumView(TemplateView):
    template_name = 'common/footer_related/impressum.html'

class ContactView(TemplateView):
    template_name = 'common/footer_related/contact.html'

class AboutView(TemplateView):
    template_name = 'common/footer_related/about.html'

@require_POST
def upload_image(request):
    print("METHOD:", request.method)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    try:
        content_file = process_image_to_webp(uploaded_file)
        path = default_storage.save(content_file.name, content_file)
        url = default_storage.url(path)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"location": url})