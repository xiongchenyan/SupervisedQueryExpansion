'''
Created on Mar 18, 2014

@author: cx
'''


from FeatureFromSERP import *

class CooccurPairQueryTermC(FeatureFromSERPC):
    
    def Init(self):
        self.UWSize = 15
        
        
    def __init__(self,ConfIn = ""):
        super(CooccurPairQueryTermC,self).__init__(ConfIn)
        self.Init()
        
    
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
        
        ExpTerm.hFeature['CooccurPairQTermPRF'] = self.CountValueForDocs(ExpTerm, lPSFDoc) / float(self.TotalLen(lPSFDoc))
        ExpTerm.hFeature['CooccurPairQTermCorp'] = self.CountValueForDocs(ExpTerm, lBgDoc) / float(self.TotalLen(lBgDoc))
        
        return True                
        
    
    def CountValueForDocs(self,ExpTerm,lDoc):
        value = 0.0
        PairCnt = 0.0
        lQTerm = ExpTerm.query.split()
        
        
        for doc in lDoc:
            vCol = doc.GetContent().split()
            for i in range(len(lQTerm)):
                for j in range(i+1,len(lQTerm)):
                    if lQTerm[i] == lQTerm[j]:
                        continue
                    PairCnt += 1
                    lTerm = [lQTerm[i],lQTerm[j],ExpTerm.term]
                    value += UW(vCol,lTerm,self.UWSize)
        if 0 != PairCnt:
            value /= PairCnt
        return value
                    