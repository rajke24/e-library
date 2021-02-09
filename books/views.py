from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Book, Genre
from .forms import OpinionCreateForm


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
    opinions = book.opinions.all()

    def update_book_rating():
        rating = 0
        opinions = book.opinions.all()
        for opinion in opinions:
            rating += opinion.rating
        book.rating = round(rating / len(opinions), 2)
        book.save()

    if request.method == 'POST':
        if opinions.filter(author=request.user).exists():
            messages.warning(request, "Cannot add another review. You have already reviewed this book!")
            return redirect(f'/book/{id}/')
        form = OpinionCreateForm(request.POST)

        if form.is_valid():
            new_opinion = form.save(commit=False)
            new_opinion.author = request.user
            new_opinion.book = book
            new_opinion.save()
            update_book_rating()
            messages.success(request, "Review succesfully added!")
            return redirect(f'/book/{id}/')
    else:
        form = OpinionCreateForm()

    return render(request, 'books/book_details.html', {'book': book})
