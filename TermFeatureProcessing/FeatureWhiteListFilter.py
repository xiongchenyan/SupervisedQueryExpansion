'''
Created on Aug 4, 2014
filter by white list
in: expterm + name
out: expterm result
@author: cx
'''


import site
import pickle

site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from base.ExpTerm import *

import sys
if 4 != len(sys.argv):
    print "expterm + feature name + out"
    sys.exit()
    
llExpTerm = ReadQExpTerms(sys.argv[1])
hName = {}
for line in open(sys.argv[2]):
    hName[line.strip()] = True
    
llExpTerm = FilterFeatureViaWhiteList(llExpTerm,hName)
DumpQExpTerms(llExpTerm,sys.argv[3])
