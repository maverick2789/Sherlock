# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:55:10 2016
@Title: WordNet API
@author: Proactive Panda
"""
#Imports
from collections import Counter as cn

from nltk.corpus import wordnet as wn
import operator
import gensim
import word2VecAPI



def fetch_parents(word,n):
    
    if n == 0:
        return None
    synobj = wn.synsets(word)
    parents = {}
    vocab = get_vocab_freq()

    if len(synobj) > 0 :
        syn =synobj[0] #Initial Assumption
        parobj = syn.hypernyms()
        for par in parobj:
            par_word = par.name().split('.')[0]
            parents[par_word] = vocab[par_word]
            pardict = fetch_parents(par_word,n-1)
            if pardict != None:
                parents.update(pardict)
                
        parents = sorted(parents.items(), key=operator.itemgetter(1),reverse = True)
        return parents
    else:
        return None
        
        
def fetch_pos_parents(word,n,pos_tag):
    synobj = wn.synsets(word)
    if len(synobj) > 0 :
        for syn in synobj:
            if syn.pos() == pos_tag:
                syn_word = syn.name().split('.')[0]
                parents = fetch_parents(syn_word,n)
                break
        
        return parents
    else:
        return None

def fetch_class(word):
    synobj = wn.synsets(word)
    if len(synobj) > 0 :
        syn = synobj[0] #Initial Assumption
        class_name = syn.lexname()
        class_name = class_name.split('.')[1]
        return class_name
    else:
        return None
    
def fetch_synonyms(word):
    synobj = wn.synsets(word)
    synonyms = []
    if len(synobj) > 0 :
        for syn in synobj:
            for word in syn.lemmas():
                synonyms.append(word.name())
        return synonyms
    else:
        return None
        
def fetch_antonyms(word):
    synobj = wn.synsets(word)
    antonyms = []
    if len(synobj) > 0 :
        for syn in synobj:
            for word in syn.lemmas():
                if word.antonyms():
                    antonyms.append(word.antonyms()[0].name())
        return antonyms
    else:
        return None

def fetch_children(word,n):
    
    if n == 0:
        return None
    synobj = wn.synsets(word)
    children = {}
    vocab = get_vocab_freq()

    if len(synobj) > 0 :
        syn =synobj[0] #Initial Assumption
        childobj = syn.hyponyms()
        for child in childobj:
            child_word = child.name().split('.')[0]
            children[child_word] = vocab[child_word]
            pardict = fetch_children(child_word,n-1)
            if pardict != None:
                children.update(pardict)
                
        children = sorted(children.items(), key=operator.itemgetter(1),reverse = True)
        return children
    else:
        return None




#############MAIN
#Trials
#obj = fetch_parents('cyan',4)
#obj = fetch_pos_parents('run',3,'n')
#obj1 = fetch_synonyms('view')
#obj2 = fetch_antonyms('view')
#obj = fetch_children('green',3)