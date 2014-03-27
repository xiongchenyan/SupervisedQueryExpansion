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

from base.ExpTerm import *
from cxBase.base import *
from FeatureHash import *


import sys


if 1 > len(sys.argv):
    print "1 para: conf file"
    print "in\nout\nfeaturenamedict\npositivebar"
    sys.exit()
    
conf = cxConf(sys.argv[1])

InName = conf.GetConf('in')
OutName = conf.GetConf('out')
DictName = conf.GetConf('featurenamedict')
PosBar = float(conf.GetConf('positivebar'))
llExpTerm = ReadQExpTerms(InName,)
lExpTerm = []
for mid in llExpTerm:
    lExpTerm.extend(mid)

lExpTerm = InitizeFeature(lExpTerm,DictName)
lExpTerm = BinarizeScore(lExpTerm,PosBar)
out = open(OutName,'w')
for ExpTerm in lExpTerm:
    print >> out,ExpTerm.dump()
    
out.close()