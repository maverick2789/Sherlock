# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:28:53 2016

@author: avi
"""

# Returns anaphora resolved text 
from pycorenlp import StanfordCoreNLP
import json



def anaphora(text):
   nlp = StanfordCoreNLP('http://192.168.54.210:9000/')
   output = nlp.annotate(text, properties={
  'annotators': 'tokenize,ssplit,dcoref',
  'outputFormat': 'json'
  })
  
   print(output['sentences'][0]['parse'])
   #out = json.loads(output)
   with open("C:\\Users\\avi\\Desktop\\Sherlock\\Books\\jsonDemo.txt", "w") as outfile:
    json.dump(output, outfile)
  
text = ( 'Ram and shyam are good boys. they like icecream.')
anaphora(text)
  