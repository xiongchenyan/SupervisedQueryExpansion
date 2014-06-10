'''
Created on Jun 10, 2014

full extraction of ObjFeatures
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from FbFeatureExtraction.FreebasePrfFeatureExtraction import *
from FbFeatureExtraction.FreebaseObjLevelFeatureExtraction import *
from FbFeatureExtraction.FreebaseQueryLevelFeatureExtraction import *

import sys
from cxBase.Conf import cxConfC


if 2 != len(sys.argv):
    print "conf"
    FreebasePrfFeatureExtractionC.ShowConf()
    FreebaseObjLevelFeatureExtractionC.ShowConf()
    FreebaseQueryLevelFeatureExtractionC.ShowConf()
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])


InName = conf.GetConf('in')
OutName = conf.GetConf('out')

PrfExtractor = FreebasePrfFeatureExtractionC(sys.argv[1])
ObjExtractor = FreebaseObjLevelFeatureExtractionC(sys.argv[1])
QExtractor = FreebaseQueryLevelFeatureExtractionC(sys.argv[1])


llExpTerm = ReadQExpTerms(InName)

out = open(OutName,'w')
for lExpTerm in llExpTerm:
    lExpTerm = PrfExtractor.ExtractForOneQ(lExpTerm)
    lExpTerm = ObjExtractor.ExtractForOneQ(lExpTerm)
    lExpTerm = QExtractor.ExtractForOneQ(lExpTerm)
    for ExpTerm in lExpTerm:
        print >>out, ExpTerm.dumps()
        
out.close()
print "finished"


