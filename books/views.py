from django.shortcuts import render

# Create your views here.
def library(request):
    return render(request, 'books/library.html', {'title': 'Library'})