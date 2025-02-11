from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mama_to_be import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mama_to_be.common.urls')),
    path('profile/', include('mama_to_be.profiles.urls')),
    path('article/', include('mama_to_be.articles.urls')),
    path('forum/', include('mama_to_be.forum.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
