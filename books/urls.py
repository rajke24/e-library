from django.urls import path
from .views import library


urlpatterns = [
    path('library/', library, name='library'),
]