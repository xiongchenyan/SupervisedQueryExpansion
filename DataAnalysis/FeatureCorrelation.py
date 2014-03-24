'''
Created on Mar 20, 2014
pearson of feature and label
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
import json

import sys


  
def FeatureCorrelationAnalysis(lExpTerm):
    #get all feature name
        #record all score
    #for each feature  get all its value's, in order, if not exist, add 0
    #get pearson  
    
    
    hFeatureValue = {}
    lScore = []
    
    for ExpTerm in lExpTerm:
        lScore.append(ExpTerm.score)
        for feature in ExpTerm.hFeature:
            hFeatureValue[feature] = []
    
    for ExpTerm in lExpTerm:
        for feature in hFeatureValue:
            value = 0
            if feature in ExpTerm.hFeature:
                value = ExpTerm.hFeature[feature]
            hFeatureValue[feature].append(value)
    
    hFeaturePearson = {}
    for feature in hFeatureValue:
        hFeaturePearson[feature] = pearson(lScore,hFeatureValue[feature])
        
    return hFeaturePearson

if 3 != len(sys.argv):
    print "term features in + out"
    sys.exit()
    
lExpTerm = []
for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    lExpTerm.append(ExpTerm)
    
hFeatureCoor = FeatureCorrelationAnalysis(lExpTerm)
out = open(sys.argv[2],'w')
print >>out,json.dumps(hFeatureCoor,indent=1)
out.close()