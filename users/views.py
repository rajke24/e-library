from django.shortcuts import render

def login_page(request):
    return render(request, 'users/login.html', {'title': 'Log in'})


def register(request):
    return render(request, 'users/register.html', {'title': 'Register'})