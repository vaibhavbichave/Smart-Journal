from django.shortcuts import render
from .recommender import recommendation
from pathlib import Path
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
