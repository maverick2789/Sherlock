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
    
def questionParser(text):
    text = preprocess(text)
    
