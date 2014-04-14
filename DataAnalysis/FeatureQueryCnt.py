'''
Created on Apr 14, 2014
count the number of query each feature appears
input: expansion term feature
output: feature\t # distinct q
@author: cx
'''


'''
1: read exp terms
2: reverse to a feature->{qid} dict (hope fit in memory, submit to condor not on head node)
3: collect feature cnt, sort, output 
'''

import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
from operator import itemgetter
from CalcFeatureQueryCnt import *

if 3 != len(sys.argv):
    print "2 para: exp term feature + output feature query cnt"
    sys.exit()

hFeatureCnt =  CalcFeatureQueryCnt(sys.argv[1])
lFeatureCnt = hFeatureCnt.items()
    
lFeatureCnt.sort(key=itemgetter(1),reverse=True)
out = open(sys.argv[2],'w')
for item in lFeatureCnt:
    print >>out, item[0] + "\t%d" %(item[1])
out.close()
                        

print "finished"           
