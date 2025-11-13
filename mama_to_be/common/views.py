from django.views.generic import TemplateView


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
