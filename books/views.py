from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Book, Genre, BookInstance, BookReservation
from .forms import OpinionCreateForm


def library(request):
    book_list = Book.objects.all().order_by('title')
    genres = Genre.objects.all().order_by('name')

    context = {
        'title': 'Library',
        'book_list': book_list,
        'genres': genres,
    }

    return render(request, 'books/library.html', context)


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    opinions = book.opinions.all()

    def get_available_book():
        book_instances = BookInstance.objects.filter(book=book, status="AVAILABLE")
        return book_instances[0] if book_instances else None

    def update_book_rating():
        rating = 0
        opinions = book.opinions.all()
        for opinion in opinions:
            rating += opinion.rating
        book.rating = round(rating / len(opinions), 2)
        book.save()
    
    def add_opinion(form):
        new_opinion = form.save(commit=False)
        new_opinion.author = request.user
        new_opinion.book = book
        new_opinion.save()
        update_book_rating()

    book_instance = get_available_book()
    if request.method == 'POST':
        # add opinion
        if 'post_opinion' in request.POST:
            # check if user already added opinion about this book
            if opinions.filter(author=request.user).exists():
                messages.warning(request, "Cannot add another review. You have already reviewed this book!")
                return redirect(f'/library/book/{id}/')

            form = OpinionCreateForm(request.POST)
            if form.is_valid():
                add_opinion(form)
                messages.success(request, "Review succesfully added!")
                return redirect(f'/library/book/{id}/')
        elif 'reserve' in request.POST:
            bookReservation = BookReservation.objects.create(
                book=book_instance, booker=request.user)
            book_instance.status = "RESERVED"
            book_instance.save()
            messages.success(request, "Book succesfully reserved!", extra_tags="successful_reservation")
            book_instance = get_available_book()
    else:
        form = OpinionCreateForm()

    return render(request, 'books/book_details.html', {'book': book, 'book_instance': book_instance})


def is_valid_queryparam(param):
    return param != '' and param is not None


def book_filter_view(request):
    books = Book.objects.all()
    book_title = request.GET.get('book_title')
    book_author = request.GET.get('book_author')
    book_genre = request.GET.get('book_genre')
    book_rating = request.GET.get('book_rating')

    sort_method = request.GET.get('sort')

    genres = Genre.objects.all().order_by('name')
    searched = False
    most_popular = False

    if is_valid_queryparam(book_title):
        books = books.filter(title__icontains=book_title).order_by('title')
        searched = True
    elif is_valid_queryparam(book_author):
        books = books.filter(author__last_name__icontains=book_author) | books.filter(
            author__first_name__icontains=book_author)
        books = books.order_by('title')
        searched = True
    if is_valid_queryparam(book_genre):
        books = books.filter(genre__name=book_genre)

    if is_valid_queryparam(sort_method):
        if sort_method == 'popularity':
            books = books.order_by('-rating')
            most_popular = True
        else:
            books = books.order_by(sort_method)

    context = {
        'book_list': books,
        'genres': genres,
        'searched': searched,
        'genre': book_genre,
        'popularity_ranking': most_popular,
    }

    return render(request, 'books/library.html', context)
