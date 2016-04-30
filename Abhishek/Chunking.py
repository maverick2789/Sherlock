# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:13:56 2016

@author: Sanchari
"""
import nltk
import re
import string
from nltk import pos_tag, word_tokenize

def np_chunk(sent):
    #f=open('D:/MTECH/4th sem/ir/project/Free.High.School.Science.Texts.PDF-OpenSci/test_bio.txt','rb')
    #text=f.read()
    #preprocess
    sent=preprocess(sent)
    nG = r"""
    NP: 
    {<DT|PRP\$>?<JJ>*<NN>+} 
    {<NNP>+}
    {<DT|PRP\$>?<JJ>*<NNS>+}
    {<NN>+}
    """
    vG="VP:{<VBP>*<VBN>*}"
    cp = nltk.RegexpParser(nG)
    cp2=nltk.RegexpParser(vG)
    #text=preprocess(text)
    #sents=nltk.sent_tokenize(text)
    #print 'checking random:',sents[9]
    #for sent in sents:
    #sent = ''.join(ch for ch in sent if ch not in set(string.punctuation))
    tagged=nltk.pos_tag(sent.split())
    result = cp.parse(tagged)
    print 'noun phrase :',result
    #print type(result)
    result.draw()
    res2=cp2.parse(tagged)
    #print 'now verb phrase:',res2
    #return result,res2
    #res2.draw()
    #f.close() 
    #return sents,result

def preprocess(text):
    text=text.replace('\r\n','')
    text=text.replace('\n','')
    text=re.sub(' +',' ',text)
    text=re.sub(r'[^\x00-\x7F]+','', text)
    #text=re.sub(ur"[^\w\d'\s-]+",'',text)
    return text
np_chunk('I shot an elephant in my pajamas')
#np_chunk('Charles Darwin in 1859, published his famous work "Origin of species"')
#np_chunk('As per the State Forest Report 1999, based on visual and satellite data from IRS-1B, 1C and 1D, the total forest cover of India is 637,293 sq. km.')
#np_chunk('The pure air the water the animals the plants the microbes and human beings are interlinked in a life sustaining system called the environment.')

#did not work..stanford parser partial code
#from nltk.parse.stanford import StanfordDependencyParser
#path_to_jar = 'C:/Users/Sanchari/Anaconda/stanford-parser-full-2015-12-09/stanford-parser.jar'
#path_to_models_jar = 'C:/Users/Sanchari/Anaconda/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
#dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
#result = dependency_parser.raw_parse('I shot an elephant in my sleep')