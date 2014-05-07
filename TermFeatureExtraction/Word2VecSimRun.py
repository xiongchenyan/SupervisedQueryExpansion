'''
Created on May 6, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/TermFeatureExtraction')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from TermFeatureExtraction.Word2VecSim import *

import sys
if 2 != len(sys.argv):
    print "conf:\n"
    QueryExpTermWord2VecSimFeatureExtractorC.ShowConf()
    sys.exit()
    
    
Extractor = QueryExpTermWord2VecSimFeatureExtractorC(sys.argv[1])

Extractor.Process()

print "finished"
