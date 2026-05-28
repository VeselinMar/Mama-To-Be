from django.urls import path

from mama_to_be.common.views import HomeView, PrivacyView, ImpressumView, contact_view, AboutView, search_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacy/', PrivacyView.as_view(), name='privacy_policy'),
    path('impressum/', ImpressumView.as_view(), name='impressum'),
    path('contact/', contact_view, name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path("search/", search_view, name="search"),

]
