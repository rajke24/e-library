from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import UserRegistrationForm

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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account successfully created.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'title': 'Register', 'form': form})
