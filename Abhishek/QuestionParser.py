# -*- coding: utf-8 -*-
"""
Created on Sun May 01 03:20:10 2016

@author: avi
"""
import re
import string
from nltk import pos_tag, word_tokenize
text = 'what is the name of the bacteria that smokes weed?'

def preprocess(text):
    text=text.replace('\r\n','')
    text=text.replace('\n','')
    text=re.sub(' +',' ',text)
    text=re.sub(r'[^\x00-\x7F]+','', text)
    #text=re.sub(ur"[^\w\d'\s-]+",'',text)
    return text

def whWordExtractor(text):
    try:
        whType = ''
        whPattern = re.compile(r'who|what|where|when|whom|whose|', re.IGNORECASE)
        whMatch = whPattern.search(text)
        if whMatch:
                    whWord = whMatch.group()
                    print whWord
                    if whWord in ['who','whom','whose']:
                        whType = 'person'
                    elif whWord in ['when']:
                        whType = 'date'
                    elif whWord in ['where']:
                        whType = 'location'
        return whType        
    except IOError:
        pass
    
  
def questionParser(text):
    text = preprocess(text)
    whType = whWordExtractor(text)
    text = pos_tag(text.split())
    nouns,verbs=[],[]
    for each in text:
        if 'NN' in each[1]:
            nouns.append(each[0])
        elif 'V' in each[1]:
            verbs.append(each[0])
    print nouns , verbs , whType
    
    
questionParser('when did shyam go to the moon?')    
    
    
    
