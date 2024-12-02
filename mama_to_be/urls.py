"""
URL configuration for mama_to_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mama_to_be import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mama_to_be.common.urls')),
    path('profile/', include('mama_to_be.profiles.urls')),
    path('article/', include('mama_to_be.articles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
