'''
Created on Apr 14, 2014
count the number of query each feature appears
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import ExpTermC,ReadQExpTerms

def CalcFeatureQueryCnt(InData):

    hFeatureQid = {}
    
    if type(InData) == str:
        llExpTerm = ReadQExpTerms(InData)
    else:
        llExpTerm = InData
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            for feature in ExpTerm.hFeature:
                if not feature in hFeatureQid:
                    hFeatureQid[feature] = []
                if not ExpTerm.qid in hFeatureQid[feature]:
                    hFeatureQid[feature].append(ExpTerm.qid)
    
    hFeatureCnt = {}
    for feature in hFeatureQid:
        hFeatureCnt[feature] = len(hFeatureQid[feature])
        
    return hFeatureCnt


