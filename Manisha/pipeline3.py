# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 02:48:03 2016

@author: Salazar
"""
def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        print term
    
def process_sent_insert_db(sent):
    toks=sent.split()
    postoks = nltk.pos_tag(toks)
    print postoks  
    tree = chunker.parse(postoks)
    print tree
    tree.draw()
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        #print 'subtree:',subtree
        leaves= subtree.leaves()
        #print 'leaves ',leaves
        if len(leaves)==1: #be sure its only a noun..hence node without property
            node_word=wordnet_lemmatizer.lemmatize(leaves[0][0])
            print 'will create node ',node_word
            #graphAPI.insert_node(client,node_word)
        else: #maybe adj/noun followed by noun
            #properties=[a[0] for a in leaves if a[1]=='JJ']
            properties=[['type',a[0]] for a in leaves[:-1]]
            node_word=wordnet_lemmatizer.lemmatize(leaves[-1][0])
            print 'will create node ',node_word,properties
            #graphAPI.insert_node(client,node_word,properties)

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#import graphAPI

text="""England was inhabited for many centuries before its written history began.  
The earliest races that possessed the country were stunted, brutal savages.  
They used pieces of rough flint for tools and weapons.  From flint too they produced fire.  
They lived by hunting and fishing, and often had no homes but caves and rock shelters."""
lemmatizer = nltk.WordNetLemmatizer()
grammar = r"""
    #NBAR:
    #    {<DT>?<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
    TP:
    {<DT>|<W.*>|<IN>}
    NP: 
   {<PRP\$>?<JJ.*>*<NN>+} 
   {<NNP>+}
   {<PRP\$>?<JJ.*>*<NNS>+}
   {<NN>+}
   COMBONP:   
   {<NP|COMBONP>+<CC><NP|COMBONP>+}
   COMBONP2:   
   {<NP|COMBONP>+<CC><NP|COMBONP>+}
        
#    NP:
#        {<NBAR>}
#        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        
    VP:
        {<TP>*<VB.?>?<TP>*<VB.?>*<TP>*}
    adv:
        {<RB.*>}
    NUM:{<CD>}
    
    NVN:
        {<NP|COMBONP|COMBONP2><VP><NP|COMBONP|COMBONP2>}
"""
chunker = nltk.RegexpParser(grammar)
wordnet_lemmatizer = WordNetLemmatizer()
#client=graphAPI.open_db()    

#main work starts here
text=nltk.sent_tokenize(text)
for sent in text:
    process_sent_insert_db(sent)
        

    
#obj = graphAPI.fetch_thing(client,'animal')


    
    
