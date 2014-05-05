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

import sys


if 3 > len(sys.argv):
    print "2 para: input + outname + (positivebar default 0)"
    sys.exit()
    

InName = sys.argv[1]
OutName = sys.argv[2]
DictName = OutName + "_initdict"
PosBar = 0
if len(sys.argv) >= 4:
    PosBar = float(sys.argv[3])





llExpTerm = ReadQExpTerms(InName)
print "read term from [%s] done" %(InName)
llExpTerm = DiscardSingleQFeature(llExpTerm)
print "discard feature that only appear in one q done"
lExpTerm = []
for mid in llExpTerm:
    lExpTerm.extend(mid)

lExpTerm = InitizeFeature(lExpTerm,DictName)
print "initize feature done"
lExpTerm = BinarizeScore(lExpTerm,PosBar)
print "binarizescore done"
out = open(OutName,'w')
for ExpTerm in lExpTerm:
    print >> out,ExpTerm.dump()
    
out.close()
print "finished"