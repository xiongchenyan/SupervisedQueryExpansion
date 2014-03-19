'''
Created on Mar 18, 2014
function to extract all feature from SERP
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from TermDistributionSERP import *
from CooccurSingleQueryTerm import *
from CooccurPairQueryTerm import *
from WeightedTermProximity import *
from  DocFreqForQTermsAndExpTermsCoor import *

def SERPFeatureExtractionFullFunc(ConfIn,lExpTerm,lDoc = []):
    print "start extract feature for q [%s] [%d] terms" %(lExpTerm[0].query,len(lExpTerm))
    TermDist = TermDistributionSERPC(ConfIn)
    CoorSingle = CooccurSingleQueryTermC(ConfIn)
    CoorPair = CooccurPairQueryTermC(ConfIn)
    WTermProx = WeightedTermProximityC(ConfIn)
    DocFreqForCoor = DocFreqForQTermsAndExpTermsCoorC(ConfIn)
    
    
    TermDist.ExtractForQuery(lExpTerm, lDoc)
    CoorSingle.ExtractForQuery(lExpTerm, lDoc)
    CoorPair.ExtractForQuery(lExpTerm, lDoc)
    WTermProx.ExtractForQuery(lExpTerm,lDoc)
    DocFreqForCoor.ExtractForQuery(lExpTerm, lDoc)
    print "features extracted"
    return True
    
    
class SERPFeatureExtractFullC:
    def Init(self):
        return
    
    def SetConf(self,ConfIn):
        self.TermDist = TermDistributionSERPC(ConfIn)
        self.CoorSingle = CooccurSingleQueryTermC(ConfIn)
        self.CoorPair = CooccurPairQueryTermC(ConfIn)
        self.WTermProx = WeightedTermProximityC(ConfIn)
        self.DocFreqForCoor = DocFreqForQTermsAndExpTermsCoorC(ConfIn)
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
            
    def Process(self,lExpTerm,lDoc):
        self.TermDist.ExtractForQuery(lExpTerm, lDoc)
        self.CoorSingle.ExtractForQuery(lExpTerm, lDoc)
        self.CoorPair.ExtractForQuery(lExpTerm, lDoc)
        self.WTermProx.ExtractForQuery(lExpTerm,lDoc)
        self.DocFreqForCoor.ExtractForQuery(lExpTerm, lDoc)
        return True