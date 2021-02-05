from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

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
    if request.method == 'POST':
        profile_form = ProfileUpdateFrom(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'Your account profile has been updated successfully!'
                )
            return redirect('profile')
    else:
        profile_form = ProfileUpdateFrom(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile_edit.html')
