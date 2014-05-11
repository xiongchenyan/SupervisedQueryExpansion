'''
Created on May 11, 2014
just do filtering
@author: cx
'''


import site
import pickle

site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from base.ExpTerm import *
from cxBase.base import *
from TermFeatureProcessing.FeatureHash import *
from TermFeatureProcessing.DiscardSingleQFeature import DiscardSingleQFeature
from cxBase.FeatureBase import cxFeatureC
import sys


if 3 > len(sys.argv):
    print "2 para: input + outname  filter fraction min (default 0.01)"
    sys.exit()
    

InName = sys.argv[1]
OutName = sys.argv[2]
DictName = OutName + "_initdict"
PosBar = 0
MinFilterFrac = 0.01
if len(sys.argv) >= 4:
    MinFilterFrac = float(sys.argv[4])




llExpTerm = ReadQExpTerms(InName)
print "read term from [%s] done" %(InName)
lExpTerm = []
for mid in llExpTerm:
    lExpTerm.extend(mid)

lExpTerm = cxFeatureC.FilterByFraction(lExpTerm, MinFilterFrac)
print "filter dim by min frac [%f] done" %(MinFilterFrac)

out = open(OutName,'w')
for ExpTerm in lExpTerm:
    print >> out,ExpTerm.dump()
    
out.close()
print "finished"