from django.urls import path

from mama_to_be.common import views

urlpatterns = [
    path('', views.home, name='home')
]