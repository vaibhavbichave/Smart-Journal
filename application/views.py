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
from application.models import Profile, ProfileEntries, ProfileMood, CustomProfile
import os
import math
import pandas as pd
import pickle
from django.views.decorators.csrf import csrf_exempt
from application.prediction import predict_deep, loaded_model


# index = []
# pickle.dump(index, open('index.pkl', 'wb'))
df = pd.read_csv('static/dataset/data_moods.csv')

df_happy = df[df.mood == 'Happy']
df_calm = df[df.mood == 'Calm']
df_sad = df[df.mood == 'Sad']
df_energetic = df[df.mood == 'Energetic']


@login_required
def songs(request):
    user = User.objects.get(username=request.user.username)
    profile = ProfileMood.objects.filter(user=user).first()
    emotion_data = {}
    # {'sadness': 0, 'joy': 1, 'surprise': 2,'love': 3, 'anger': 4, 'fear': 5}
    # emotion_data['sadness'] = profile.sadness
    # emotion_data['joy'] = profile.joy
    # emotion_data['surprise'] = profile.surpise
    # emotion_data['love'] = profile.love
    # emotion_data['anger'] = profile.anger
    # emotion_data['fear'] = profile.fear
    # N = 10
    # happy_songs = 0
    # calm_songs = 0
    # energetic_songs = 0
    # sad_songs = 0

    # sorted_emotion_data = dict(
    #     sorted(emotion_data.items(), key=lambda x: x[1], reverse=True))

    # for emotion, emo_val in sorted_emotion_data.items():

    #     curr_val = int(emo_val+5/10)
    #     if (N - int(curr_val) < 0):
    #         curr_val = N
            
    #     if (emotion == 'sadness'):
    #         sad_songs += int(curr_val)

    #     elif (emotion == 'joy' or emotion == 'surprise'):
    #         res_val = int(curr_val/2)
    #         energetic_songs += int(math.ceil(curr_val - res_val))
    #         happy_songs += res_val

    #     elif (emotion == 'love' or emotion == 'fear'):
    #         calm_songs += int(curr_val)

    #     elif (emotion == 'anger'):
    #         res_val = int(curr_val/2)
    #         energetic_songs += int(math.ceil(curr_val - res_val))
    #         calm_songs += res_val

    #     else:
    #         continue

    #     N = N - int(curr_val)


    # print(happy_songs, sad_songs, calm_songs, energetic_songs)
    # print(sorted_emotion_data)

    dataframe = {}
    df1 = df_happy.sample(n=int(profile.happy_songs))
    df2 = df_calm.sample(n=int(profile.calm_songs))
    df3 = df_energetic.sample(n=int(profile.energetic_songs))
    df4 = df_sad.sample(n=int(profile.sad_songs))

    df1 = pd.concat([df1, df2, df3, df4])

    for i in df1.index:
        data = {}

        data['name'] = df1.loc[i, "name"]
        data['id'] = "https://open.spotify.com/embed/track/" + \
            df1['id'][i] + "?utm_source=generator"
        data['artist'] = df1['artist'][i]
        data['mood'] = df1['mood'][i]
        dataframe[i] = data
    df2 = {}
    df2['data'] = dataframe
    return render(request, 'songs.html', df2)


@login_required
def result(request):
    # file = open("index.pkl", "rb")
    # index = pickle.load(file)
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.filter(user=user).first()
    song = '1999'
    if (profile.music):
        song = profile.music
    index = recommendation(song, 'cosine')
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
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.filter(user=user).first()
        profile.music = song
        profile.save()
        # index = recommendation(song, 'cosine')

        # pickle.dump(index, open('index.pkl', 'wb'))
        return result(request)
    return result(request)


@login_required
def journal(request):
    user = User.objects.get(username=request.user.username)
    # profile = Profile.objects.filter(user=user).first()
    context = {
        "journalText": "",#profile.text,
    }
    return render(request, 'journal.html', context)


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
                profile = CustomProfile.objects.create(user=user)
                profileMood = ProfileMood.objects.create(user=user)
                # profile.first_name = request.POST['first_name'] 
                # profile.last_name = request.POST['last_name']
                # profile.email = request.POST['email']
                # profile.gender = request.POST['gender']
                # profile.age = request.POST['age']
                user.save()
                profile.save()
                profileMood.save()
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
        # profile = ProfileEntries.objects.filter(user=user).first()
        profile = ProfileEntries.objects.create(user=user)
        profile.sadness = percents[0]
        profile.joy = percents[1]
        profile.surpise = percents[2]
        profile.love = percents[3]
        profile.anger = percents[4]
        profile.fear = percents[5]
        profile.text = entry
        profile.save()

        emotion_data = {}
        # {'sadness': 0, 'joy': 1, 'surprise': 2,'love': 3, 'anger': 4, 'fear': 5}
        emotion_data['sadness'] = profile.sadness
        emotion_data['joy'] = profile.joy
        emotion_data['surprise'] = profile.surpise
        emotion_data['love'] = profile.love
        emotion_data['anger'] = profile.anger
        emotion_data['fear'] = profile.fear

        N = 10
        happy_songs = 0
        calm_songs = 0
        energetic_songs = 0
        sad_songs = 0

        sorted_emotion_data = dict(
            sorted(emotion_data.items(), key=lambda x: x[1], reverse=True))

        for emotion, emo_val in sorted_emotion_data.items():

            curr_val = int(emo_val+5/10)
            if (N - int(curr_val) < 0):
                curr_val = N
                
            if (emotion == 'sadness'):
                sad_songs += int(curr_val)

            elif (emotion == 'joy' or emotion == 'surprise'):
                res_val = int(curr_val/2)
                energetic_songs += int(math.ceil(curr_val - res_val))
                happy_songs += res_val

            elif (emotion == 'love' or emotion == 'fear'):
                calm_songs += int(curr_val)

            elif (emotion == 'anger'):
                res_val = int(curr_val/2)
                energetic_songs += int(math.ceil(curr_val - res_val))
                calm_songs += res_val

            else:
                continue

            N = N - int(curr_val)

        profile = ProfileMood.objects.filter(user=user).first()
        profile.happy_songs = happy_songs
        profile.sad_songs = sad_songs
        profile.calm_songs = calm_songs
        profile.energetic_songs = energetic_songs
        profile.save()
        print(happy_songs, sad_songs, calm_songs, energetic_songs)
        print(sorted_emotion_data)

        # index = recommendation(song, 'cosine')
        # pickle.dump(index, open('index.pkl', 'wb'))
        # return render(request, 'login.html')
        return redirect("/dashboard/")
        # return render(request, "song.html", {xx=mood, yy=percents})
    return render(request, 'login.html')


def dashboard(request):
    user = User.objects.get(username=request.user.username)
    user_profile = ProfileEntries.objects.filter(user=user)
    print (len(user_profile))
    if len(user_profile)>5:
        user_profile = ProfileEntries.objects.filter(user=user).order_by('-id')[:5][::-1]
    print(user_profile)
    profile = ProfileEntries.objects.filter(user=user).last()
    if profile is None:
        return redirect('/login/')
    
    emotions = {}
    emo_sad = []
    emo_joy = []
    emo_love = []
    emo_surprise = []
    emo_anger = []
    emo_fear = []
    for entry in user_profile:
        emo_sad.append(entry.sadness)
        emo_joy.append(entry.joy)
        emo_love.append(entry.love)
        emo_surprise.append(entry.surpise)
        emo_anger.append(entry.anger)
        emo_fear.append(entry.fear)

    emotions['sad'] = emo_sad
    emotions['joy'] = emo_joy
    emotions['surprise'] = emo_surprise
    emotions['love'] = emo_love
    emotions['anger'] = emo_anger
    emotions['fear'] = emo_fear

    percents = [profile.sadness, profile.joy, profile.surpise,
                profile.love, profile.anger, profile.fear]
    data = {}
    data['name'] = user.username
    data['journalText'] = profile.text
    data['yy'] = percents


    return render(request, 'dashboard.html', {**data, **emotions})

def previousEntry(request):
    user = User.objects.get(username=request.user.username)
    user_profile = ProfileEntries.objects.filter(user=user).order_by('-id')[:5][::1]
    prev_entries = []
    for entry in user_profile:
        prev_entries.append(entry.text)

    data = {}
    data['entries'] = prev_entries
    # print(prev_entries)
    return render(request, 'previousEntry.html', data)