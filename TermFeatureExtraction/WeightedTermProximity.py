'''
Created on Mar 18, 2014

@author: cx
'''

from FeatureFromSERP import *

class WeightedTermProximityC(FeatureFromSERPC):
    def Init(self):
        self.UWSize = 12
        
        
    def __init__(self,ConfIn = ""):
        super(WeightedTermProximityC,self).__init__(self,ConfIn)
        self.Init()
        
        
    def MaxDocLen(self,lDoc):
        if [] == lDoc:
            return 0
        res = lDoc[0].GetLen()
        for doc in lDoc[1:]:
            res = max(doc.GetLen(),res)
        return res
    
    def dist(self,qterm,term,lDoc):
        #get the min distance between qterm and term
        MinDist = self.MaxDocLen(lDoc)
        for doc in lDoc:
            vCol = doc.GetContent().split()
            mid = MinDist(vCol,qterm,term)
            if -1 == mid:
                continue
            MinDist = min(mid,MinDist)
        return MinDist
    
    def Coor(self,qterm,term,lDoc):
        res = 0
        for doc in lDoc:
            res += UW(doc.GetContent().split(),[qterm,term],self.UWSize)
        return res
    
    
    def CalcForDocs(self,ExpTerm,lDoc):
        lQTerm = ExpTerm.query.split()
        value = 0
        WSum = 0
        term = ExpTerm.term
        for qterm in lQTerm:
            coor = self.Coor(qterm,term,lDoc)
            value +=  coor * self.dist(qterm,term,lDoc) 
            WSum += coor
        if WSum != 0:
            value /= WSum
        return value
    
    
    def ExtractForTerm(self,ExpTerm,lPSFDoc,lBgDoc):
        ExpTerm.hFeature['WeightedTermProximityPRF'] = self.CalcForDocs(ExpTerm, lPSFDoc) 
        ExpTerm.hFeature['WeightedTermProximityCorp'] = self.CalcForDocs(ExpTerm, lBgDoc)
        return True
            