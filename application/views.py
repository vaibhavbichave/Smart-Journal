from django.shortcuts import render, redirect
from application.recommender import recommendation
from application.prediction import predict_deep, loaded_model
from pathlib import Path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login, logout
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from application.models import Profile
import os
import pandas as pd
import pickle
from django.views.decorators.csrf import csrf_exempt
from application.prediction import predict_deep, loaded_model


index = []
pickle.dump(index, open('index.pkl', 'wb'))
df = pd.read_csv('static/dataset/data_moods.csv')


@login_required
def songs(request):
    dataframe = {}
    for i in range(len(df)):
        data = {}
        data['name'] = df['name'][i]
        data['id'] = "https://open.spotify.com/embed/track/" + \
            df['id'][i] + "?utm_source=generator"
        data['artist'] = df['artist'][i]
        data['mood'] = df['mood'][i]
        dataframe[i] = data
    df2 = {}
    df2['data'] = dataframe
    return render(request, 'songs.html', df2)


@login_required
def result(request):
    file = open("index.pkl", "rb")
    index = pickle.load(file)
    dataframe = {}
    for i in index:
        data = {}
        data['name'] = df['name'][i]
        data['id'] = "https://open.spotify.com/embed/track/" + \
            df['id'][i] + "?utm_source=generator"
        data['artist'] = df['artist'][i]
        data['mood'] = df['mood'][i]
        dataframe[i] = data
    df2 = {}
    df2['data'] = dataframe
    return render(request, 'result.html', df2)


@login_required
def test(request):
    if request.method == "GET":
        song = list(request.GET.keys())[0]
        index = recommendation(song, 'cosine')
        
        pickle.dump(index, open('index.pkl', 'wb'))
        return result(request)
    return result(request)


@login_required
def journal(request):
    return render(request, 'journal.html')


@login_required
def homepage(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                profile = Profile.objects.create(user=user)
                user.save()
                profile.save()
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'signup.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'signup.html')


@login_required
def custom_logout(request):
    logout(request)
    request.session.flush()
    messages.info(request, "Logged out successfully")
    return redirect('login')


def custom_login(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'login.html')


@csrf_exempt
def predictMood(request):
    if request.method == "POST":
        entry = request.POST['entry']
        percents, mood = predict_deep(entry, loaded_model)
        print(percents)

        # emotions =   {'sadness': 0, 'joy': 1, 'surprise': 2,'love': 3, 'anger': 4, 'fear': 5}
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.filter(user=user).first()
        profile.sadness = percents[0]
        profile.joy = percents[1]
        profile.surpise = percents[2]
        profile.love = percents[3]
        profile.anger = percents[4]
        profile.fear = percents[5]
        profile.text = entry
        profile.save()

        # index = recommendation(song, 'cosine')
        # pickle.dump(index, open('index.pkl', 'wb'))
        # return render(request, 'login.html')
        return redirect("/dashboard/")
        # return render(request, "song.html", {xx=mood, yy=percents})
    return render(request, 'login.html')
   

def dashboard(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.filter(user=user).first()
    if profile is None:
        return redirect('/login/')
    percents =[profile.sadness,profile.joy,profile.surpise ,profile.love ,profile.anger ,profile.fear]
    data={}
    data['yy'] = percents
    return render(request,'dashboard.html',data)