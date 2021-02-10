from django.urls import path
from .views import elibrary, ebook_details, ebook_filter_view, download_ebook

urlpatterns = [
    path('elibrary/', elibrary, name='elibrary'),
    path('elibrary/search/', ebook_filter_view, name='filter_ebook'),
    path('ebook/<int:pk>/', ebook_details, name='ebook_details'),
    path('ebook/downloaded/<int:pk>/', download_ebook, name='download_ebook'),
]
