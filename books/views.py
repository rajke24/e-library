from django.shortcuts import render, get_object_or_404

from .models import Book, Genre

def library(request):
    bookList = Book.objects.all().order_by('title')
    genres = Genre.objects.all().order_by('name')

    context = {
        'title': 'Library',
        'bookList': bookList,
        'genres': genres,
    }

    return render(request, 'books/library.html', context)

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    return render(request, 'books/book_details.html', {'book': book})