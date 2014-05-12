'''
Created on May 12, 2014
calc query cnt and run
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
import sys

from DataAnalysis.CalcFeatureQueryCnt import *


if 3 != len(sys.argv):
    print "qexp term input + output feature appear q cnt"
    sys.exit()
    
hFeatureCnt = CalcFeatureQueryCnt(sys.argv[1])


l = hFeatureCnt.items()
l.sort(Key=lambda item:item[1],reverse=True)
out = open(sys.argv[2],'w')
for item in l:
    print >> out,item[0] + "\t%d" %(item[1])
out.close()
print "finished"