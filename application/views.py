from django.shortcuts import render
from . import recommender

from pathlib import Path
import os
import pandas as pd

def index(request):
        
    df = pd.read_csv('static/dataset/data_moods.csv')
    dataframe = {}
    for i in range(len(df)):
        data = {}
        data['name'] = df['name'][i]
        data['artist'] = df['artist'][i]
        data['mood'] = df['mood'][i]
        dataframe[i]=data

    # print(d)
        # dataframe[i] =  data
    # print(dataframe)
    df2 = {}
    df2['data'] = dataframe
    return render(request,'index.html', df2)

def result(request):
    return render(request,'result.html')