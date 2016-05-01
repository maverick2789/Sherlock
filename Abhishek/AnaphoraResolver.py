# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:28:53 2016

@author: avi
"""

# Returns anaphora resolved text 
from pycorenlp import StanfordCoreNLP
import json
import nltk

def sentenceRange(string):
    string = string.replace('(','').replace(')','').replace('[','').replace(']','')
    string = string.split(',')
    return int(string[0]) , int(string[2]) , int(string[3]) 

def fromTo(string):
    string.replace(' ','')
    string = string.split('->')
    print string
    return string[0] , string[1]

def NERGetter(text):
    nlp = StanfordCoreNLP('http://192.168.54.210:9000/')
    output = nlp.annotate(text, properties={
    'annotators': 'tokenize,ssplit,pos , ner',
    'outputFormat': 'text'})
    output = str(output.replace('\r','').replace('\t',''))
    output = output.split('[', 1)[1]
    output = str(output)
    output = output.split('\n')
    for i in output[0:-1]:
        i = i.replace(']','')
        i = i.split('NamedEntityTag=')
    return i[1]
def anaphora(text):
   
   nlp = StanfordCoreNLP('http://192.168.54.210:9000/')
   output = nlp.annotate(text, properties={
  'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
  'outputFormat': 'text'})
   sents = nltk.sent_tokenize(text) 
   a=[]
   for sent in sents:   
       a.append(sent.split())
   
   output = output.split('Coreference set:', 1)[1]
   output = str(output.replace('\r','').replace('\t',''))
   output = output.split('\n');
   for i in output[1:-1]:
       i = i.split(', that is:')
       toFrom = i[0].split('->')
       fromSent , fromStart, fromEnd = sentenceRange(toFrom[0])
       toSent , toStart, toEnd = sentenceRange(toFrom[1])
       fromText , toText = fromTo(i[1])
       a[fromSent - 1][fromStart - 1:fromEnd - 1] = a[toSent - 1][toStart - 1:toEnd - 1]  
       
   return a
  
#anaphora(text)
print NERGetter('New York')
  