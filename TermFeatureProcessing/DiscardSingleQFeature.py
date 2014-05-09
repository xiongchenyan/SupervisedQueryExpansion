'''
Created on Apr 14, 2014
discard feature the only appear in one query
@author: cx
'''


import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from DataAnalysis.CalcFeatureQueryCnt import *



import json


def DiscardSingleQFeature(llExpTerm):
    hFeatureCnt = CalcFeatureQueryCnt(llExpTerm)
#     print "feature query cnt:\n%s" %(json.dumps(hFeatureCnt,indent=1))
    llRes = []
    for lExpTerm in llExpTerm:
        lNewExpTerm = []
        for ExpTerm in lExpTerm:
            hNewFeature = {}
            for feature in ExpTerm.hFeature:
                if hFeatureCnt[feature] > 1:
                    hNewFeature[feature] = ExpTerm.hFeature[feature]
            ExpTerm.hFeature = dict(hNewFeature)
            lNewExpTerm.append(ExpTerm)
        llRes.append(lNewExpTerm)
    return llRes




