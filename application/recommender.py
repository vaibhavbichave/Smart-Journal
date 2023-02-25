import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors

from pathlib import Path
import os

data = pd.read_csv('static/dataset/data_moods.csv')
label_encoder = LabelEncoder()
data.mood = label_encoder.fit_transform(data['mood'])

feature_cols = ['energy', 'loudness', 'valence', 'danceability',
                'acousticness', 'instrumentalness', 'speechiness', 'tempo', 'mood']
normalized = preprocessing.normalize(data[feature_cols])
normalized = pd.DataFrame(normalized, columns=feature_cols)
normalized['mean'] = normalized.mean(axis=1)


# Finding Out If Song Is Present In DataSet
def getSongIndex(songName):

    bool = data['name'].isin([songName])
    # Getting Index Of Song If Present
    sindex = bool[bool == True].index[0]
    return sindex


linear_kernal = linear_kernel(normalized)
euclidian = euclidean_distances(normalized)
cosine = cosine_similarity(normalized)


def recommendation(songName, model_Name):
    model = cosine
    if model_Name == 'linear':
        model = linear_kernal
    elif model_Name == 'euclidean':
        model = euclidian
    SongIndex = getSongIndex(songName)
    score = list(enumerate(model[SongIndex]))
    sim_score = sorted(score, key=lambda x: x[1], reverse=True)
    sim_score = sim_score[1:11]
    Index = [i[0] for i in sim_score]
    return Index


feature_cols = data.drop([
    'name', 'album', 'artist', 'id', 'release_date'], axis=1)
X = feature_cols


neigh = NearestNeighbors(n_neighbors=10, algorithm='brute')
neigh.fit(X)


def KNNRecommendation(SongName):
    Y = data.iloc[getSongIndex(SongName)]
    Y = Y.drop([
        'name', 'album', 'artist', 'id', 'release_date'])
    test_Y = pd.DataFrame(data=Y, index=None)
    test_Y = test_Y.T
    distances, indices = neigh.kneighbors(test_Y)
    for i in range(1, len(distances.flatten())):
        print('{0}: {1}, with a distance of {2}.'.format(
            i, data['name'].iloc[indices.flatten()[i]], distances.flatten()[i]))


# print("\nrecommendation using linear - ")
# print(recommendation('Alison', 'linear'))


# print("\nrecommendation using euclidian - ")
# print(recommendation('Alison', 'euclidian'))


# print("\nrecommendation using cosine - ")
# print(recommendation('Alison', 'cosine'))


# print("\nrecommendation using KNN - ")
# KNNRecommendation('Alison')
