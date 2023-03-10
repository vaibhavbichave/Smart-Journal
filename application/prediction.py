import pickle
import numpy as np
from flask import Flask, request, render_template
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import model_from_json
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings
warnings.filterwarnings('ignore')


def get_key(value):
    for key, val in emotions.items():
        if (val == value):
            return key


def remove_stopwords(sentence):
    text_tokens = word_tokenize(sentence)
    tokens_without_sw = [
        word for word in text_tokens if not word in stopwords.words('english')]
    return (" ").join(tokens_without_sw)


def predict_deep(sentence, model):
    sentence = remove_stopwords(sentence.lower())
    sentence_lst = []
    sentence_lst.append(sentence)
    sentence_seq = tokenizer.texts_to_sequences(sentence_lst)
    sentence_padded = pad_sequences(sentence_seq, maxlen=80, padding='post')
    certaintyprediction = model.predict(sentence_padded)[0]
    rescertainity = [round(x*100) for x in certaintyprediction]
    bestpredictionindex = np.argmax(certaintyprediction)
    certainty = str(round(certaintyprediction[bestpredictionindex]*100, 2))
    return [rescertainity, get_key(bestpredictionindex)]


emotions = {'sadness': 0, 'joy': 1, 'surprise': 2,
            'love': 3, 'anger': 4, 'fear': 5}

tokenizer_file = open("static/model/tokenizer.pkl", "rb")
tokenizer = pickle.load(tokenizer_file)
tokenizer_file.close()

json_file = open('static/model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("static/model/model.h5")

