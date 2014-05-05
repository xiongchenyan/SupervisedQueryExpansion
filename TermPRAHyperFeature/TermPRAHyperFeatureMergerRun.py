'''
Created on Apr 29, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')

from TermPRAHyperFeature.TermPRAHyperFeatureMerger import TermPRAHyperFeatureMergerC

import sys

if 2 != len(sys.argv):
    print "conf:"
    TermPRAHyperFeatureMergerC().ShowConf()
    sys.exit()
    
    
merger = TermPRAHyperFeatureMergerC(sys.argv[1])
merger.Process()
print "finished"
