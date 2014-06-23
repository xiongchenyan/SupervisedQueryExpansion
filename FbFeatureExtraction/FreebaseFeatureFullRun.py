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
from FreebaseCateKLFeatureExtraction import *


import sys
from cxBase.Conf import cxConfC


if 2 != len(sys.argv):
    print "conf"
    FreebasePrfFeatureExtractionC.ShowConf()
    FreebaseObjLevelFeatureExtractionC.ShowConf()
    FreebaseQueryLevelFeatureExtractionC.ShowConf()
    FreebaseCateKLFeatureExtractionC.ShowConf()
    print "needprf true\nneedobjlvl false\nneedqlvl false\nneedcatekl true"
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])


NeedPrf = bool(conf.GetConf('needprf'))
NeedObjLvl = bool(conf.GetConf('needobjlvl'))
NeedQLvl = bool(conf.GetConf('needqlvl'))
NeedCateKL = bool(conf.GetConf('needcatekl'))


InName = conf.GetConf('in')
OutName = conf.GetConf('out')

if NeedPrf:
    PrfExtractor = FreebasePrfFeatureExtractionC(sys.argv[1])
if NeedObjLvl:
    ObjExtractor = FreebaseObjLevelFeatureExtractionC(sys.argv[1])
if NeedQLvl:
    QExtractor = FreebaseQueryLevelFeatureExtractionC(sys.argv[1])
if NeedCateKL:
    CateKLExtractor = FreebaseCateKLFeatureExtractionC(sys.argv[1])


llExpTerm = ReadQExpTerms(InName)

out = open(OutName,'w')
for lExpTerm in llExpTerm:
    if NeedPrf:
        lExpTerm = PrfExtractor.ExtractForOneQ(lExpTerm)
    if NeedObjLvl:
        lExpTerm = ObjExtractor.ExtractForOneQ(lExpTerm)
    if NeedQLvl:
        lExpTerm = QExtractor.ExtractForOneQ(lExpTerm)
    if NeedCateKL:
        lExpTerm = CateKLExtractor.ExtractForOneQ(lExpTerm)
    for ExpTerm in lExpTerm:
        print >>out, ExpTerm.dumps()
        
out.close()
print "finished"


