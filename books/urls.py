from django.urls import path
from .views import library, book_detail


urlpatterns = [
    path('library/', library, name='library'),
    path('book/<int:id>/', book_detail, name='bookDetails'),
]