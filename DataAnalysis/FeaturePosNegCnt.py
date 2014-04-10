'''
Created on Apr 10, 2014
calculate the prob(cnt?) of feature in positive term, in negative term, and minus
@author: cx
'''





import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
import json
import sys
import math
from operator import itemgetter


if 3 != len(sys.argv):
    print "exp term +output"
    sys.exit()

hFeatureCnt={} #feature str ->[pos,neg]


TotalPos = 0
TotalNeg = 0
for line in open(sys.argv[1]):
    ExpTerm = ExpTermC(line.strip())
    for Feature in ExpTerm.hFeature:
        if not Feature in hFeatureCnt:
            hFeatureCnt[Feature] = [0,0]
        if ExpTerm.score > 0:
            TotalPos += 1
            hFeatureCnt[Feature][0] += 1
        else:
            TotalNeg += 1
            hFeatureCnt[Feature][1] += 1
            
out = open(sys.argv[2],'w')
lFeature = []
for feature in hFeatureCnt:
    value = hFeatureCnt[feature]
    value[0] = (value[0] / float(TotalPos)) * 1000
    value[1] = (value[1]/ float(TotalNeg)) * 1000
    lFeature.append([feature] + value + [value[0] - value[1]])
    print >>out, feature + "\t%f\t%f\t%f" %(value[0],value[1],value[0]-value[1])
    
out.close()

out = open(sys.argv[2] + "_TopPos",'w')
lFeature.sort(key=itemgetter(1), reverse=True)
lTop = lFeature[0:1000]
for top in lTop:
    print >>out, "%s\t%f\t%f\t%f" %(top[0],top[1],top[2],top[3])
    
out.close()

out = open(sys.argv[2] + "_TopNeg",'w')
lFeature.sort(key=itemgetter(2), reverse=True)[0:1000]
lTop = lFeature[0:1000]
for top in lTop:
    print >>out, "%s\t%f\t%f\t%f" %(top[0],top[1],top[2],top[3])
    
out.close()


out = open(sys.argv[2] + "_TopDiff",'w')
lFeature.sort(key=itemgetter(3), reverse=True)[0:1000]
lTop = lFeature[0:1000]
for top in lTop:
    print >>out, "%s\t%f\t%f\t%f" %(top[0],top[1],top[2],top[3])
    
out.close()    