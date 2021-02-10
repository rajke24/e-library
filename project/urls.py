from django.conf import settings
from project import settings as media_settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from landing.views import home

admin.site.site_title = "Library Administration"
admin.site.site_header = "Library Administration"
admin.site.site_index = "Library "

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('users.urls')),
    path('', include('books.urls')),
    path('', include('ebooks.urls')),
]

if settings.DEBUG:
    urlpatterns += static(media_settings.MEDIA_URL,
                          document_root=media_settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
