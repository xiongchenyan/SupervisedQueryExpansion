'''
Created on Mar 18, 2014
extract features from SERP
    mainly from Guihong's paper
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
import math
from cxBase.base import *
from IndriRelate.IndriPackedRes import *
from base.ExpTerm import *
class FeatureFromSERPC(object):
    def Init(self):
        self.CashDir = ""
        self.TotalSERPNum = 1000
        self.PSFDocNum = 20
        self.BgDocNum = 100 #the number of tail docs used as background
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.CashDir = conf.GetConf("cashdir")
        self.TotalSERPNum = int(conf.GetConf('totalserpnum'))
        self.PSFDocNum = int(conf.GetConf("numofserpdoc"))
        self.BgDocNum = int(conf.GetConf('bgdocnum'))
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if ("" != ConfIn):
            self.SetConf(ConfIn)
    
    
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
        #main function to implement for sub-classes, fill the hFeature dict in ExpTerm
        print "call my subclass"
        return False
        
    def ExtractForQuery(self,lExpTerm,lDoc=[]):
        if len(lExpTerm)==0:
            return True
        lPSFDoc,lBgDoc = self.ReadDoc(lExpTerm[0].query,lDoc)
        
        for ExpTerm in lExpTerm:
            self.ExtractForTerm(ExpTerm, lPSFDoc, lBgDoc)      
        self.ProtectedLogFeatureValue(lExpTerm)  
        MinMaxFeatureNormalize(lExpTerm)        
        return True
        
        
    def ReadDoc(self,query,lDoc=[]):
        if len(lDoc) < self.TotalSERPNum:
            lDoc =ReadPackedIndriRes(self.CashDir + "/" + query,self.TotalSERPNum)
        lPSFDoc = lDoc[:self.PSFDocNum]
        lBgDoc = lDoc[len(lDoc) - self.PSFDocNum:]
        return lPSFDoc,lBgDoc                   
    
    
    def TotalLen(self,lDoc):
        cnt = 0
        for doc in lDoc:
            cnt += doc.GetLen()
        return cnt
    
    
    def ProtectedLogFeatureValue(self,lExpTerm):
        for i in range(len(lExpTerm)):
            for feature in lExpTerm[i].hFeature:
                lExpTerm[i].hFeature[feature] = ProtectedLog(lExpTerm[i].Feature[feature])
        return True
        
        