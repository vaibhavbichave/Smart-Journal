from django.shortcuts import render
from . import recommender

def index(request):
    return render(request,'index.html')

def result(request):
    return render(request,'result.html')