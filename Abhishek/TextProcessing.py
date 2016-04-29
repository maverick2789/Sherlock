# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 22:11:41 2016

@author: avi
"""

import Chunking
import nltk
result,res2=Chunking.np_chunk('Charles Darwin in 1859, published his famous work "Origin of species"')
for a in result:
        #if type(a) is nltk.Tree:
            if a.node == 'NP': # This climbs into your NVN tree
                print a.leaves()