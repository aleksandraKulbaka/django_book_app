from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1> Blog home </h1>')

    # Create your views here.
def about(request):
    return HttpResponse('<h1> This is Blog About page </h1>')