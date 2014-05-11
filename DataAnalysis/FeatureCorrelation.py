'''
Created on Mar 20, 2014
pearson of feature and label
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
from base.ExpTerm import *
from ResultAnalysis.PearsonCoefficient import pearson
import json

import sys
from operator import itemgetter
import math

  
def FeatureCorrelationAnalysis(lExpTerm,RandomInfluenceBound):
    #get all feature name
        #record all score
    #for each feature  get all its value's, in order, if not exist, add 0
    #get pearson  
    
    
    hFeatureValue = {}
    lScore = []
    InCnt = 0
    for ExpTerm in lExpTerm:
        if math.fabs(ExpTerm.score) <= RandomInfluenceBound:
            continue
        InCnt += 1
        lScore.append(ExpTerm.score)
        for feature in ExpTerm.hFeature:
            hFeatureValue[feature] = []
    
    for ExpTerm in lExpTerm:
        if math.fabs(ExpTerm.score) <= RandomInfluenceBound:
            continue
        for feature in hFeatureValue:
            value = 0
            if feature in ExpTerm.hFeature:
                value = ExpTerm.hFeature[feature]
            hFeatureValue[feature].append(value)
    
    hFeaturePearson = {}
    for feature in hFeatureValue:
        hFeaturePearson[feature] = pearson(lScore,hFeatureValue[feature])
    print "total [%d] expterm, keep [%d]" %(len(lExpTerm),InCnt)
    return hFeaturePearson

if 3 > len(sys.argv):
    print "term features in + out + discard to small influence bound (default 0)"
    sys.exit()

RandomInfluenceBound = 0

lExpTerm = []
for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    lExpTerm.append(ExpTerm)
    
hFeatureCoor = FeatureCorrelationAnalysis(lExpTerm,RandomInfluenceBound)
out = open(sys.argv[2],'w')

lRes = hFeatureCoor.items()
lRes.sort(key = lambda item: math.fabs(item[1]),reverse = True)
for res in lRes:
    print >>out,'%s\t%f'%(res[0],res[1])
out.close()