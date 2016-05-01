# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:28:53 2016

@author: avi
"""

# Returns anaphora resolved text 
from pycorenlp import StanfordCoreNLP
from nltk import pos_tag, word_tokenize
import json

def sentenceRange(string):
    string = string.replace('(','').replace(')','').replace('[','').replace(']','')
    string = string.split(',')
    return int(string[0]) , int(string[2]) , int(string[3]) 

def fromTo(string):
    string.replace(' ','')
    string = string.split('->')
    #print string
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
    
def shorten(text):
    text = ''.join(i for i in text if i.isalnum() or i.isspace())
    text = pos_tag(text.split())
    for each in text:
        if 'NN' in each[1]:
            return each[0]
    
def anaphora(text):
   
   nlp = StanfordCoreNLP('http://192.168.54.210:9000/')
   output = nlp.annotate(text, properties={
  'annotators': 'tokenize,ssplit,pos,depparse,parse,coref',
  'outputFormat': 'text'})
   sents = nltk.sent_tokenize(text) 
   a=[]
   for sent in sents:   
       a.append(sent.split())
   output = str(output.replace('\r','').replace('\t',''))  
   #output = output.split('Coreference set:', 1)[1]
   output = output.split('Coreference set:')
   #output = str(output.replace('\r','').replace('\t',''))
   #output = output.split('\n');
   for out in output[1:]:
       #print out
       out = str(out.replace('\r','').replace('\t',''))
       out = out.split('\n')
       for i in out[1:-1]:
           i = i.split(', that is:')
           toFrom = i[0].split('->')
           fromSent , fromStart, fromEnd = sentenceRange(toFrom[0])
           toSent , toStart, toEnd = sentenceRange(toFrom[1])
           fromText , toText = fromTo(i[1])
           
           if len(toText.split()) > 1:
              toText = shorten(toText)
              toText = [toText]
           #a[fromSent - 1][fromStart - 1:fromEnd - 1] = a[toSent - 1][toStart - 1:toEnd - 1]
              a[fromSent - 1][fromStart - 1:fromEnd - 1] = toText
   return a
print anaphora('England is a nice country. England was inhabited for many centuries before its written history began. The earliest races that possessed the country were stunted, brutal savages. They used pieces of rough flint for tools and weapons.  From flint too they produced fire. They lived by hunting and fishing, and often had no homes but caves and rock shelters.')  
#print anaphora('England is a nice country. England was inhabited for many centuries before its written history began. The earliest races that possessed the country were stunted, brutal savages. They used pieces of rough flint for tools and weapons.  From flint too they produced fire.They lived by hunting and fishing, and often had no homes but caves and rock shelters.')
#print NERGetter('19th january')
  