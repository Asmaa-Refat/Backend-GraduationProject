# -*- coding: utf-8 -*-
"""SentimentAnalysis_GPModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N9CfbzUwAg6jaWMqD49dllvjrJHzI4s6
"""

#python version: 3.11.0
#pip install django
#pip install djangorestframework
#pip install emoji --upgrade
#pip install PyArabic
#pip install nltk
#pip install -U scikit-learn
#pip install pandas
# pip install django-cors-headers


import re
import sys
import nltk
import emoji
import string
import argparse
import numpy as np
import pandas as pd
#import missingno as msno
import pyarabic.araby as araby
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix,accuracy_score, classification_report, f1_score

#nltk.download('stopwords')
#nltk.download('punkt')
import os
df = pd.read_csv('ModelApp/MachineModel/Sentiment_Dataset.csv')
df.head()

def remove_emoji(text):
    return emoji.demojize(text)

def cleaning(text):
 Arabic_numbers = ['٤','١','٢','٣','٥','٦','٧','٨','٩','٠']
 special_character = ['؟','،','?',',','!','.',':','"','""','‘‘','‘','؛','↓',"'", '‰',
                      '`','€',';','ç','ı','À','@','٬','~᷂','٫','.','ـ',''
                      '=','#','$','%','^','&','*','()',')','(','\\','/','~','¦'
                      '((', '_', '"','"', '…','-','×','ツ','+','÷','٪', '{', '}', '[',']', '<', '>','|']
 #remove emojis 
 text= remove_emoji(text)
 #replace special characters with whitespaces 
 for word in range(0, len(special_character)):
     text = text.replace(special_character[word], ' ') 
 #replace arabic numbers with whitespaces 
 for word in range(0, len(Arabic_numbers)):
     text = text.replace(Arabic_numbers[word], ' ') 
 #remove english words letters and numbers
 text = re.sub(r'[0-9a-zA-Z]+',' ', text)

 return text

def stop_word_removal(text):
 stop_words = set(stopwords.words("arabic"))
 words = araby.tokenize(text)
 text = " ".join([w for w in words if not w in stop_words])
 return text

def normalization(text):
#replace Ta'a and Hamza'a and Ya'a
 text = re.sub("[إأٱآا]", "ا", text)
 text = re.sub("ى", "ي", text)
 text = re.sub("ة", "ه", text)
#remove extra whitespace
 text = re.sub('\s+', ' ', text)   
#remove tashkeel
 text = araby.strip_tashkeel(text)
 return text

def pre_processing(text):
 #Cleaning
 text = cleaning(text)
 #stop words removal
 text = stop_word_removal(text)
 #Normalization 
 text = normalization(text)
 #stop words removal
 text = stop_word_removal(text)
 return text

#pre_processing the review column
df['Review']  = df['Review'].apply(lambda x:pre_processing(x))

def process_text(text):
    stemmer = nltk.ISRIStemmer()
    word_list = nltk.word_tokenize(text)
    #stemming
    word_list = [stemmer.suf32(w) for w in  word_list]
    return ' '.join(word_list)

#lemmatization the review column
df['Review']  = df['Review'].apply(lambda x:process_text(x))
df['Review']

df["Classification"].value_counts()

#remove tabs and new lines from the text 
df['Review'] = df.Review.str.replace("\xa0"," ") 
df['Review'] = df.Review.str.replace("\n"," ")
df['Review'] = df['Review'].replace("\t"," ", regex=True)

# check for nulls 
df['Review'].isnull().sum()
#remove blanks by replacing them with Nan
df['Review'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
# drop nans
df.dropna(subset=['Review'], inplace=True)

# drop duplicates 
df=df.drop_duplicates(subset=['Review'])
# shuffling the data
df = df.sample(frac = 1)
# splitting into train and tests
X_train, X_test, Y_train, Y_test = train_test_split(df['Review'], df['Classification'], test_size =0.2, random_state=100)

# assemble several steps that can be cross-validated together while setting different parameters.
pipe = make_pipeline(TfidfVectorizer(), MultinomialNB())
#pipe = make_pipeline(CountVectorizer(), MultinomialNB())

pipe.fit(X_train,Y_train)
prediction = pipe.predict(X_test)
#print("f1 Score -> ",f1_score(Y_test,prediction,average='micro')*100)

def prediction(text):
  text = pre_processing(text)
  text = process_text(text)
  list = [text]
  prediction = pipe.predict(list)
  return prediction

#print(prediction("  مش وحش  "))