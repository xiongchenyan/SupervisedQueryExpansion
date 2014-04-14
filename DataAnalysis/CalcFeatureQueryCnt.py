'''
Created on Apr 14, 2014
count the number of query each feature appears
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import ExpTermC

def CalcFeatureQueryCnt(InName):

    hFeatureQid = {}
    for line in open(InName):
        ExpTerm = ExpTermC(line.strip())
        for feature in ExpTerm.hFeature:
            if not feature in hFeatureQid:
                hFeatureQid[feature] = []
            if not ExpTerm.qid in hFeatureQid[feature]:
                hFeatureQid[feature].append(ExpTerm.qid)
    
    hFeatureCnt = {}
    for feature in hFeatureQid:
        hFeatureCnt[feature] = len(hFeatureQid[feature])
        
    return hFeatureCnt