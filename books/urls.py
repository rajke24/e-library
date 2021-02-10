from django.urls import path
from .views import library, book_detail, book_filter_view


urlpatterns = [
    path('library/', library, name='library'),
    path('library/book/<int:id>/', book_detail, name='bookDetails'),
    path('library/search/', book_filter_view, name='filter_book'),
]
