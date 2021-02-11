import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from books.models import BookInstance, BookReservation, BookRental
from .forms import UserRegistrationForm, ProfileUpdateFrom, UserUpdateForm
from .decorators import is_unauthenticated, is_allowed


@is_unauthenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, "Wrong username/email or password")
            return redirect('login')

    return render(request, 'users/login.html', {'title': 'Log in'})

@is_unauthenticated
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='reader')
            user.groups.add(group)
            user.save()
            messages.success(request, 'Account successfully created.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'title': 'Register', 'form': form})


@login_required
@is_allowed(allowed_groups=['reader'])
def profile(request):
    return render(request, 'users/profile.html')


@login_required
@is_allowed(allowed_groups=['reader'])
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileUpdateFrom(request.POST, request.FILES, instance=user.profile)
        user_form = UserUpdateForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your account profile has been updated successfully!'
                )
            return redirect('profile')
    else:
        profile_form = ProfileUpdateFrom(instance=user.profile)
        user_form = UserUpdateForm(instance=user)

    return render(request, 'users/profile_edit.html')


@login_required(login_url='login')
@is_allowed(allowed_groups=['reader'])
def user_books(request):
    user = request.user
    book_reservations = BookReservation.objects.filter(booker=user)
    book_rentals = BookRental.objects.filter(booker=user)
    book_instance_id = request.POST.get('book_instance_id')
    book_to_extend_id = request.POST.get('book_instance_extend_id')

    def discard_reservation(book_id):
        book_instance = BookInstance.objects.get(id=book_id)
        book_instance.status = "AVAILABLE"
        book_instance.save()
        reservation = BookReservation.objects.get(book=book_instance, booker=user)
        reservation.delete()

    def extend_book_rental(book_id):
        book_instance = BookInstance.objects.get(id=book_id)
        bookRental = BookRental.objects.get(book=book_instance, booker=user)
        if bookRental.on_loan_duration < 5:
            bookRental.on_loan_duration += 1
            bookRental.save()

    if request.method == 'POST':
        if book_instance_id:
            discard_reservation(book_instance_id)
        elif book_to_extend_id:
            extend_book_rental(book_to_extend_id)
    
    context = {
        'current_data': datetime.datetime.today().date(), 
        'book_reservations': book_reservations, 
        'book_rentals': book_rentals,
        }

    return render(request, 'users/user_books.html', context)