from textblob import TextBlob
import pandas as pd
from tensorflow import keras
import re
from textblob import Word
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk
import os
import emoji
import contractions
import pickle
import numpy as np
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import model_from_json
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings
warnings.filterwarnings('ignore')

warnings.filterwarnings('ignore')
abbreviations = {
    "$": " dollar ",
    "€": " euro ",
    "4ao": "for adults only",
    "a.m": "before midday",
    "a3": "anytime anywhere anyplace",
    "aamof": "as a matter of fact",
    "acct": "account",
    "adih": "another day in hell",
    "afaic": "as far as i am concerned",
    "afaict": "as far as i can tell",
    "afaik": "as far as i know",
    "afair": "as far as i remember",
    "afk": "away from keyboard",
    "app": "application",
    "approx": "approximately",
    "apps": "applications",
    "asap": "as soon as possible",
    "asl": "age, sex, location",
    "atk": "at the keyboard",
    "ave.": "avenue",
    "aymm": "are you my mother",
    "ayor": "at your own risk",
    "b&b": "bed and breakfast",
    "b+b": "bed and breakfast",
    "b.c": "before christ",
    "b2b": "business to business",
    "b2c": "business to customer",
    "b4": "before",
    "b4n": "bye for now",
    "b@u": "back at you",
    "bae": "before anyone else",
    "bak": "back at keyboard",
    "bbbg": "bye bye be good",
    "bbc": "british broadcasting corporation",
    "bbias": "be back in a second",
    "bbl": "be back later",
    "bbs": "be back soon",
    "be4": "before",
    "bfn": "bye for now",
    "blvd": "boulevard",
    "bout": "about",
    "brb": "be right back",
    "bros": "brothers",
    "brt": "be right there",
    "bsaaw": "big smile and a wink",
    "btw": "by the way",
    "bwl": "bursting with laughter",
    "c/o": "care of",
    "cet": "central european time",
    "cf": "compare",
    "cia": "central intelligence agency",
    "csl": "can not stop laughing",
    "cu": "see you",
    "cul8r": "see you later",
    "cv": "curriculum vitae",
    "cwot": "complete waste of time",
    "cya": "see you",
    "cyt": "see you tomorrow",
    "dae": "does anyone else",
    "dbmib": "do not bother me i am busy",
    "diy": "do it yourself",
    "dm": "direct message",
    "dwh": "during work hours",
    "e123": "easy as one two three",
    "eet": "eastern european time",
    "eg": "example",
    "embm": "early morning business meeting",
    "encl": "enclosed",
    "encl.": "enclosed",
    "etc": "and so on",
    "faq": "frequently asked questions",
    "fawc": "for anyone who cares",
    "fb": "facebook",
    "fc": "fingers crossed",
    "fig": "figure",
    "fimh": "forever in my heart",
    "ft.": "feet",
    "ft": "featuring",
    "ftl": "for the loss",
    "ftw": "for the win",
    "fwiw": "for what it is worth",
    "fyi": "for your information",
    "g9": "genius",
    "gahoy": "get a hold of yourself",
    "gal": "get a life",
    "gcse": "general certificate of secondary education",
    "gfn": "gone for now",
    "gg": "good game",
    "gl": "good luck",
    "glhf": "good luck have fun",
    "gmt": "greenwich mean time",
    "gmta": "great minds think alike",
    "gn": "good night",
    "g.o.a.t": "greatest of all time",
    "goat": "greatest of all time",
    "goi": "get over it",
    "gps": "global positioning system",
    "gr8": "great",
    "gratz": "congratulations",
    "gyal": "girl",
    "h&c": "hot and cold",
    "hp": "horsepower",
    "hr": "hour",
    "hrh": "his royal highness",
    "ht": "height",
    "ibrb": "i will be right back",
    "ic": "i see",
    "icq": "i seek you",
    "icymi": "in case you missed it",
    "idc": "i do not care",
    "idgadf": "i do not give a damn fuck",
    "idgaf": "i do not give a fuck",
    "idk": "i do not know",
    "ie": "that is",
    "i.e": "that is",
    "ifyp": "i feel your pain",
    "IG": "instagram",
    "iirc": "if i remember correctly",
    "ilu": "i love you",
    "ily": "i love you",
    "imho": "in my humble opinion",
    "imo": "in my opinion",
    "imu": "i miss you",
    "iow": "in other words",
    "irl": "in real life",
    "j4f": "just for fun",
    "jic": "just in case",
    "jk": "just kidding",
    "jsyk": "just so you know",
    "l8r": "later",
    "lb": "pound",
    "lbs": "pounds",
    "ldr": "long distance relationship",
    "lmao": "laugh my ass off",
    "lmfao": "laugh my fucking ass off",
    "lol": "laughing out loud",
    "ltd": "limited",
    "ltns": "long time no see",
    "m8": "mate",
    "mf": "motherfucker",
    "mfs": "motherfuckers",
    "mfw": "my face when",
    "mofo": "motherfucker",
    "mph": "miles per hour",
    "mr": "mister",
    "mrw": "my reaction when",
    "ms": "miss",
    "mte": "my thoughts exactly",
    "nagi": "not a good idea",
    "nbc": "national broadcasting company",
    "nbd": "not big deal",
    "nfs": "not for sale",
    "ngl": "not going to lie",
    "nhs": "national health service",
    "nrn": "no reply necessary",
    "nsfl": "not safe for life",
    "nsfw": "not safe for work",
    "nth": "nice to have",
    "nvr": "never",
    "nyc": "new york city",
    "oc": "original content",
    "og": "original",
    "ohp": "overhead projector",
    "oic": "oh i see",
    "omdb": "over my dead body",
    "omg": "oh my god",
    "omw": "on my way",
    "p.a": "per annum",
    "p.m": "after midday",
    "pm": "prime minister",
    "poc": "people of color",
    "pov": "point of view",
    "pp": "pages",
    "ppl": "people",
    "prw": "parents are watching",
    "ps": "postscript",
    "pt": "point",
    "ptb": "please text back",
    "pto": "please turn over",
    "qpsa": "what happens",  # "que pasa",
    "ratchet": "rude",
    "rbtl": "read between the lines",
    "rlrt": "real life retweet",
    "rofl": "rolling on the floor laughing",
    "roflol": "rolling on the floor laughing out loud",
    "rotflmao": "rolling on the floor laughing my ass off",
    "rt": "retweet",
    "ruok": "are you ok",
    "sfw": "safe for work",
    "sk8": "skate",
    "smh": "shake my head",
    "sq": "square",
    "srsly": "seriously",
    "ssdd": "same stuff different day",
    "tbh": "to be honest",
    "tbs": "tablespooful",
    "tbsp": "tablespooful",
    "tfw": "that feeling when",
    "thks": "thank you",
    "tho": "though",
    "thx": "thank you",
    "tia": "thanks in advance",
    "til": "today i learned",
    "tl;dr": "too long i did not read",
    "tldr": "too long i did not read",
    "tmb": "tweet me back",
    "tntl": "trying not to laugh",
    "ttyl": "talk to you later",
    "u": "you",
    "u2": "you too",
    "u4e": "yours for ever",
    "utc": "coordinated universal time",
    "w/": "with",
    "w/o": "without",
    "w8": "wait",
    "wassup": "what is up",
    "wb": "welcome back",
    "wtf": "what the fuck",
    "wtg": "way to go",
    "wtpa": "where the party at",
    "wuf": "where are you from",
    "wuzup": "what is up",
    "wywh": "wish you were here",
    "yd": "yard",
    "ygtr": "you got that right",
    "ynk": "you never know",
    "zzz": "sleeping bored and tired"
}

emotions = {'sadness': 0, 'joy': 1, 'surprise': 2,
            'love': 3, 'anger': 4, 'fear': 5}


# Converting chat conversion words to normal words

def short_to_original(text):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)


chat_words_map_dict = {}
chat_words_list = []

# open short_form file and then read sentences from text file using read())
short_form_path = "static/dataset/short_form.txt"
short_form_list = open(short_form_path, 'r')
chat_words_str = short_form_list.read()
lines = chat_words_str.split("\n")

for line in lines:
    try:
        cw, cw_expanded = line.split("\t", 2)[:2]
        chat_words_list.append(cw.strip())
        chat_words_map_dict[cw.strip()] = cw_expanded.strip()
    except:
        pass
chat_words_list = set(chat_words_list)


def get_key(value):
    for key, val in emotions.items():
        if (val == value):
            return key


def convert_emoji(text):
    return emoji.demojize(text)


def convert_abbrev(word):
    return abbreviations[word.lower()] if word.lower() in abbreviations.keys() else word


def convert_abbrev_in_text(text):
    tokens = word_tokenize(text)
    tokens = [convert_abbrev(word) for word in tokens]
    text = ' '.join(tokens)
    return text


def expand_contractions(text):
    expanded_words = []
    for word in text.split():
        expanded_words.append(contractions.fix(word))
    expanded_text = ' '.join(expanded_words)
    return expanded_text


def chat_words_conversion(text):
    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)


def convert_to_lower(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = words[i].lower()
    sentence = " ".join(words)
    return sentence


def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower()
                      not in stopwords.words('english')]
    filtered_sentence = ' '.join(filtered_words)
    return filtered_sentence


def remove_non_alphanum(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    return text


def word_check(word):
    pattern = re.compile(r"(.)\1{2,}")
    sentence = pattern.sub(r"\1\1", word)
    b = TextBlob(sentence)
    return str(b.correct())


def remove_extendedwords(text):
    words = text.split()
    for i in range(len(words)):
        words[i] = word_check(words[i])
    sentence = " ".join(words)
    return sentence


def lemmatize_text(text):
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    tag_map = {'N': wordnet.NOUN, 'V': wordnet.VERB,
               'R': wordnet.ADV, 'J': wordnet.ADJ}

    lemmatized_words = []
    for word, tag in pos_tags:
        wn_tag = tag_map.get(tag[0].upper(), wordnet.NOUN)
        if wn_tag == wordnet.VERB and word.endswith('ed'):
            wn_tag = wordnet.VERB
            word = word[:-2]
        lemmatized_word = lemmatizer.lemmatize(word, pos=wn_tag)
        lemmatized_words.append(lemmatized_word)

    # join the lemmatized words back into a sentence
    lemmatized_sentence = ' '.join(lemmatized_words)

    return (lemmatized_sentence)


def predict_deep(sentence, model):
    sentence = convert_emoji(sentence)
    sentence = expand_contractions(sentence)
    sentence = chat_words_conversion(sentence)
    sentence = convert_to_lower(sentence)
    sentence = remove_stopwords(sentence)
    sentence = remove_non_alphanum(sentence)
    sentence = remove_extendedwords(sentence)
    sentence = lemmatize_text(sentence)
    sentence_lst = []
    sentence_lst.append(sentence)
    sentence_seq = tokenizer.texts_to_sequences(sentence_lst)
    sentence_padded = pad_sequences(sentence_seq, maxlen=80, padding='post')
    certaintyprediction = model.predict(sentence_padded)[0]

    rescertainity = [round(x*100) for x in certaintyprediction]
    bestpredictionindex = np.argmax(certaintyprediction)
    certainty = str(round(certaintyprediction[bestpredictionindex]*100, 2))
    return [rescertainity, get_key(bestpredictionindex)]


tokenizer_file = open("static/model/tokenizer.pkl", "rb")
tokenizer = pickle.load(tokenizer_file)
tokenizer_file.close()

loaded_model = keras.models.load_model("static/model/final_model.hdf5")
