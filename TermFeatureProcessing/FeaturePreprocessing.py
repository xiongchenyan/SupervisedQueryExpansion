'''
Created on Mar 27, 2014
do:
    binarize label
    feature -> init name

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
    print "2 para: input + outname + (positivebar default 0) + filter fraction min (default 0.01)"
    sys.exit()
    

InName = sys.argv[1]
OutName = sys.argv[2]
DictName = OutName + "_initdict"
PosBar = 0
if len(sys.argv) >= 4:
    PosBar = float(sys.argv[3])
MinFilterFrac = 0.01
if len(sys.argv) >= 5:
    MinFilterFrac = float(sys.argv[4])




llExpTerm = ReadQExpTerms(InName)
print "read term from [%s] done" %(InName)
# llExpTerm = DiscardSingleQFeature(llExpTerm)
# print "discard feature that only appear in one q done"
lExpTerm = []
for mid in llExpTerm:
    lExpTerm.extend(mid)

lExpTerm = cxFeatureC.FilterByFraction(lExpTerm, MinFilterFrac)
print "filter dim by min frac [%f] done" %(MinFilterFrac)

lExpTerm = InitizeFeature(lExpTerm,DictName)
print "initize feature done"


#add normilization
lExpTerm = MinMaxFeatureNormalize(lExpTerm) 

lExpTerm = BinarizeScore(lExpTerm,PosBar)
print "binarizescore done"
out = open(OutName,'w')
for ExpTerm in lExpTerm:
    print >> out,ExpTerm.dump()
    
out.close()
print "finished"