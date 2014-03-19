'''
Created on Mar 18, 2014
cooccurrence with single query term
@author: cx
'''


from FeatureFromSERP import *

class CooccurSingleQueryTermC(FeatureFromSERPC):
    
    def Init(self):
#         super(self).Init()
        self.UWSize = 12
        
    def __init__(self,ConfIn = ""):
        super(CooccurSingleQueryTermC,self).__init__(self,ConfIn)
        self.Init()
        
        
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
               
        ExpTerm.hFeature['CooccurSingleQTermPRF'] = float(self.GetValueForDoc(ExpTerm, lPSFDoc))/self.TotalLen(lPSFDoc)
        ExpTerm.hFeature['CooccurSingleQTermCorp'] = float(self.GetValueForDoc(ExpTerm, lBgDoc))/self.TotalLen(lBgDoc)
        return True        
        
        
    def GetValueForDoc(self,ExpTerm,lDoc):
        value = 0.0
        lQTerm = ExpTerm.query.split()
        for doc in lDoc:
            vCol = doc.GetContent().split()            
            for term in lQTerm:
                lTerm = [ExpTerm.term,term]
                value += UW(vCol,lTerm,self.UWSize)
        value /= float(len(lQTerm))
        return value
        
            
    
