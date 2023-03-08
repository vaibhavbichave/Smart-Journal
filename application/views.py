from django.shortcuts import render,redirect
from .recommender import recommendation
from pathlib import Path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login, logout
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import os
import pandas as pd
import pickle


index = []
pickle.dump(index, open('index.pkl', 'wb'))
df = pd.read_csv('static/dataset/data_moods.csv')

def index(request):
    dataframe = {}
    for i in range(len(df)):
        data = {}
        data['name'] = df['name'][i]
        data['artist'] = df['artist'][i]
        data['mood'] = df['mood'][i]
        dataframe[i] = data
    df2 = {}
    df2['data'] = dataframe
    return render(request, 'index.html', df2)


def result(request):
    file = open("index.pkl", "rb")
    index = pickle.load(file)
    dataframe = {}
    for i in index:
        data = {}
        data['name'] = df['name'][i]
        data['artist'] = df['artist'][i]
        data['mood'] = df['mood'][i]
        dataframe[i] = data
    df2 = {}
    df2['data'] = dataframe
    return render(request, 'result.html', df2)


def test(request):
    if request.method == "GET":
        song = list(request.GET.keys())[0]
        index = recommendation(song, 'cosine')
        pickle.dump(index, open('index.pkl', 'wb'))
        return result(request)
    return result(request)


def predict(request):
    return render(request, 'predict.html')

def homepage(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

def logout(request):
    
    auth.logout(request)
    request.session.flush()
    return redirect('home')



def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('login')

def custom_login(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')
    