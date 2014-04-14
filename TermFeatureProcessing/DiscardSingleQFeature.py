'''
Created on Apr 14, 2014
discard feature the only appear in one query
@author: cx
'''


import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from DataAnalysis.CalcFeatureQueryCnt import *

if 3 != len(sys.argv):
    print "2 para: input exp term + output term with filered feature"
    sys.exit()
    
    
hFeatureCnt = CalcFeatureQueryCnt(sys.argv[1])
print "calc query feature cnt done"
out = open(sys.argv[2],'w')

for line in open(sys.argv[1]):
    ExpTerm = ExpTermC(line.strip())
    hNewFeature = {}
    for feature in ExpTerm.hFeature:
        if hFeatureCnt[feature] > 1:
            hNewFeature[feature] = ExpTerm.hFeature[feature]
    ExpTerm.hFeature = dict(hNewFeature)
    print >>out, ExpTerm.dump()
    
out.close()

print "finished"