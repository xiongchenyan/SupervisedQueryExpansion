'''
Created on Jun 3, 2014
add ground truth score to exp term
in: exp term res + ground truth + num of exp term used (default 50)
out: exp term res + \t score
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from base.ExpTerm import *
from cxBase.base import cxBaseC,cxConf

import sys


def BuildTermScoreDict(InName):
    llExpTerm = ReadQExpTerms(InName)
    hTermScore = {}
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            hTermScore[ExpTerm.Key()] = ExpTerm.score
            
    return hTermScore


if 4 > len(sys.argv):
    print "3 para: exp terms + exp terms with ground truth score + out + num of exp term(default 50)"
    sys.exit()
    
    
hTermScore = BuildTermScoreDict(sys.argv[2])

llExpTerm = ReadQExpTerms(sys.argv[1])
NumOfExp = 50
if 5 <= len(sys.argv):
    NumOfExp = int(sys.argv[4])

for i in range(len(llExpTerm)):
    llExpTerm[i] = llExpTerm[i][:NumOfExp]
    
out = open(sys.argv[3],'w')

for lExpTerm in llExpTerm:
    for ExpTerm in lExpTerm:
        GroundTruth = 0
        if ExpTerm.Key() in hTermScore:
            GroundTruth = hTermScore[ExpTerm.Key()]
        ExpTerm.hFeature.clear()
        ExpTerm.hFeature['gt'] = GroundTruth
        print >>out, ExpTerm.dumps()
        
        
out.close()
print "finished"
    
            

