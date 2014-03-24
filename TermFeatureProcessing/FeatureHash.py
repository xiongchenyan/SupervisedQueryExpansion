'''
Created on Mar 20, 2014
transfer string feature name to int
and dump
and transfer back
@author: cx
'''



#start with 0 or one?


import site
import pickle

site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
from cxBase.base import *

import os


def InitizeFeature(lExpTerm,DictPath = ""):
    hName = {} #keep name
    if "" != DictPath:
        hName = pickle.load(DictPath)
    StartP = 1
    for i in range(len(lExpTerm)):
        hRes = {}
        for feature in lExpTerm[i].hFeature:
            feature = str(feature)
            p = len(hName) + StartP
            if feature in hName:
                p = hName[feature]
            else:
                hName[feature] = p
                hName[p] = feature #won't make confusion as feature must be string type
            hRes[p] = lExpTerm[i].hFeature[feature]
        lExpTerm[i].hFeature = hRes            
            
    out = open(DictPath,'w')
    pickle.dump(hName,out)
    return True


def ReverseInitFeature(lExpTerm,DictPath):
    hName = pickle.load(DictPath)
    for i in range(len(lExpTerm)):
        hRes= {}
        for feature in lExpTerm[i].hFeature:
            name = hName[int(feature)]
            hRes[name] = lExpTerm[i].hFeature[feature]
        lExpTerm[i].hFeature = hRes
    return True
    