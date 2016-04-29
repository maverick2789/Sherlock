# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:20:36 2016
@Title: Word2Vec API
@author: Proactive Panda
"""
#Imports

import re 
from nltk.corpus import stopwords

from collections import Counter as cn
import gensim
#path Configs:

book_path = 'E:/Study/Sem 3/IR/Text Books/Oliver Twist'
#MAKE SURE U CHANGE THE PATH ACCORDING TO THE REQUIREMENT
def pre_process_book():
    with open(book_path) as bookfile:
        book = bookfile.read()
    book = re.sub(r'[^a-zA-z0-9?.!\s]',' ',book) #remove all special Characters
    book = re.sub(r'[_\r\n]',' ',book) #Not sure why '_' is not getting removed above
    book = re.sub(r'[\s]+', r' ',book).lower(); #remove duplicate Spaces & convert to lower
    for stop in stopwords.words('english'):
            book = book.replace(' '+stop+' ',' ')
    sentences = re.split(r'[.!?]+',book) #Splitting based on sentences
    
    words = []
    for sente in sentences:
        words.append(sente.split())
    return words


def vocab_build():
    words = pre_process_book()
    vec = gensim.models.Word2Vec(words,size=100, min_count=2)
    return vec

def get_vocab_list():
    vec = vocab_build()
    return vec.vocab.keys()

def get_vocab_freq():
    words = pre_process_book()
    flat = [x for sublist in words for x in sublist]
    word_freq = cn(flat)
    return word_freq


##########
#obj = get_vocab_freq()
