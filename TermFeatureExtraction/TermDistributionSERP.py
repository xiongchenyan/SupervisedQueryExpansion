'''
Created on Mar 18, 2014
term distribution in serp
@author: cx
'''


from FeatureFromSERP import *
from IndriRelate.IndriInferencer import *
class TermDistributionSERPC(FeatureFromSERPC):
    #generate feature: TermDistPSF, TermDistCorp
    
    
    
    def DistCnt(self,ExpTerm,lLm):
        cnt = 0
        for lm in lLm:
            cnt += lm.GetTF(ExpTerm.term)
        return cnt
    
    
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
        lPSFLm = MakeLmForDocs(lPSFDoc)
        lBgLm = MakeLmForDocs(lBgDoc)
        
        TotalLen = self.TotalLen(lPSFDoc)
        TFCnt = self.DistCnt(ExpTerm, lPSFLm)
        ExpTerm.hFeature['TermDistPSF'] = float(TFCnt) / float(TotalLen)
        
        TotalLen = self.TotalLen(lBgLm)
        TFCnt = self.DistCnt(ExpTerm, lBgLm)
        ExpTerm.hFeature['TermDistCorp'] = float(TFCnt) / float(TotalLen)        
        return True         
