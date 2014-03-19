'''
Created on Mar 18, 2014

@author: cx
'''

from FeatureFromSERP import *

class DocFreqForQTermsAndExpTermsCoorC(FeatureFromSERPC):
    
    
    def CalcForDocs(self,ExpTerm,lDoc):
        cnt = 0
        lQTerm = ExpTerm.query.split()
        for doc in lDoc:
            vCol = doc.GetContent().split()
            if self.ContainQTerm(vCol,lQTerm) & (ExpTerm.term in vCol):
                cnt += 1
        return cnt + 0.5
        
    def ContainQTerm(self,vCol,lQTerm):
        for term in lQTerm:
            if term in vCol:
                return True
        return False
    
    
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
        ExpTerm.hFeature['DocFreqCoorPSF'] = self.CalcForDocs(ExpTerm, lPSFDoc)
        ExpTerm.hFeature['DocFreqCoorCorp'] = self.CalcForDocs(ExpTerm, lBgDoc)
        return True
    