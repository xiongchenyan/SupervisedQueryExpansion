'''
Created on June 10, 2014

extract object level features. To describe whether this object should be used as expansion
project object feature score to term:
    \sum_obj f(obj)*p(obj|term). p(obj|term) = 1/Z sum_obj lm(term|obj)
    
features:
    Facc score
    Lm score p(q|name) + p(q|desp)
    name|alias == Q
    q \in desp
    # of neighbors
    # types
    # has notable
    
    TBD:
        KL(p(cate|q)||p(cate|obj))

do:
    for each q:
        form all its obj's Lm
        and extract all its obj's feature. keep in vector
    for each term:
        calc p(obj|term) prob
        merge objs' feature
    

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import json
from FbFeatureExtraction.FreebaseFeatureExtraction import *
from cxBase.TextBase import *
from cxBase.Conf import cxConfC
from cxBase.Vector import VectorC
from IndriRelate.IndriInferencer import *
class FreebaseObjLevelFeatureExtractionC(FreebaseFeatureExtractionC):
    def Init(self):
        
#         self.lObjLm = []
        self.ThisQid = -1
#         self.lObjFeature = []
        
        self.lFaccObjLm = []
        self.lFaccObjFeature = []
        self.lGoogleObjLm = []
        self.lGoogleObjFeature = []
        
        
        super(FreebaseObjLevelFeatureExtractionC,self).Init()
    
    def CalcObjLm(self,lObj):
        lObjLm = []
        
        for obj in lObj:
            desp = obj.GetDesp()
            Lm = LmBaseC(desp)
            for term in Lm.hTermTF:
                score = Lm.GetTFProb(term) * self.CtfCenter.GetLogIdf(term)
                Lm.hTermTF[term] = score
            Lm.CalcLen()
            lObjLm.append(Lm)
        return lObjLm   
    
    
    def CalcTermObjScore(self,term,lObjLm):
        if [] == lObjLm:
            return []
        lObjScore = [1.0/len(lObjLm)] * len(lObjLm)
        
        lObjProb = [Lm.GetTFProb(term) for Lm in lObjLm]
        Total = float(sum(lObjProb))
        if 0 != Total:
            lObjScore = [pTermObj / Total for pTermObj in lObjProb]
        return lObjScore
    
    
    def ExtractForOneTerm(self,ExpTerm):
#         if not ExpTerm.qid in self.hQObj:
#             return ExpTerm
#         lObj = self.hQObj[ExpTerm.qid]
        self.ExtractObjFeatureAndCalcObjLm(ExpTerm.qid, ExpTerm.query)
        
        print "extracting ObjLvl for [%s][%s][%s]" %(ExpTerm.qid,ExpTerm.query,ExpTerm.term)
        
        ExpTerm = self.MergeObjFeatureToTermFeature(ExpTerm)
        
        return ExpTerm
        
        
    def MergeObjFeatureToTermFeature(self,ExpTerm):
        
        lFaccObjScore = self.CalcTermObjScore(ExpTerm.term, self.lFaccObjLm)
        lGoogleObjScore = self.CalcTermObjScore(ExpTerm.term, self.lGoogleObjLm)
        
        FaccFeature = VectorC()
        for i in range(len(lFaccObjScore)):
            FaccFeature += self.lFaccObjFeature[i] * lFaccObjScore[i]
        
        GoogleFeature = VectorC()
        for i in range(len(lGoogleObjScore)):
            GoogleFeature += self.lGoogleObjFeature[i] * lGoogleObjScore[i]
        
        ExpTerm.AddFeature(FaccFeature.hDim)
        ExpTerm.AddFeature(GoogleFeature.hDim)
        return ExpTerm
    
        
    def ExtractObjFeatureAndCalcObjLm(self,qid,query):
    #do the facc + search here    
        if qid == self.ThisQid:
            return
        print "preparing obj feature for query [%s][%s]" %(qid,query)
        
        
        lFaccObj = []
        if qid in self.hQFaccObj:
            lFaccObj = self.hQFaccObj[qid]
        lGoogleObj = []
        if qid in self.hQGoogleObj:
            lGoogleObj = self.hQGoogleObj[qid]
        
        self.lFaccObjLm = self.CalcObjLm(lFaccObj)
        self.lGoogleObjLm = self.CalcObjLm(lGoogleObj)
        
        del self.lFaccObjFeature[:]
        del self.lGoogleObjFeature[:]
        
        self.ThisQid = qid
        
        for obj in lFaccObj:
            FeatureVector = self.ExtractForOneObj(qid,query,obj,'Facc')
            self.lFaccObjFeature.append(FeatureVector)
        for obj in lGoogleObj:
            FeatureVector = self.ExtractForOneObj(qid, query, obj,'Google')
            self.lGoogleObjFeature.append(FeatureVector)                    
        return 

    def ExtractForOneObj(self,qid,query,obj,pre):
        FeatureVector = VectorC()
        print "extracting obj feature [%s] for [%s][%s][%s]" %(pre,qid,query,obj.GetName())
        FeatureVector.hDim.update(self.ExtractRankScore(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractLmScore(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractNameEqual(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractQInDespFrac(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractNeighborNum(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractTypeNum(qid,query,obj,pre))
        FeatureVector.hDim.update(self.ExtractHasNotable(qid,query,obj,pre))
        
        return FeatureVector
        
    
    def ExtractRankScore(self,qid,query,obj,pre):
        hFeature = {}
        hFeature['ObjLvl%sRankScore' %(pre)] = obj.GetScore()
        return hFeature
    
    
    
    
    def ExtractLmScore(self,qid,query,obj,pre):
        hFeature = {}
        NameLm = LmBaseC(obj.GetName())
        DespLm = LmBaseC(obj.GetDesp())
        Inferencer = LmInferencerC()
        score = 0.5 * Inferencer.InferQuery(query, NameLm, self.CtfCenter)
        score += 0.5 * Inferencer.InferQuery(query,DespLm,self.CtfCenter)
        hFeature['ObjLvl%sLmScore' %(pre)] = score
        return hFeature
    
    def ExtractNameEqual(self,qid,query,obj,pre):
        hFeature = {}
        
        lName = [obj.GetName()] + obj.GetAlias()
        lName = [TextBaseC.RawClean(text) for text in lName]
        score = 0
        target = TextBaseC.RawClean(query)
        if target in lName:
            score = 1.0
        hFeature['ObjLvl%sNameEqualQuery' %(pre)] = score
        return hFeature    
    
    def ExtractQInDespFrac(self,qid,query,obj,pre):
        hFeature = {}
        
        desp = TextBaseC.RawClean(obj.GetDesp())
        lQTerm =  TextBaseC.RawClean(query).split()
        score = 0
        for term in lQTerm:
            if term in desp:
                score += 1
        hFeature['ObjLvl%sQInDespFrac' %(pre)] = score / len(lQTerm)
        return hFeature 
    
    def ExtractNeighborNum(self,qid,query,obj,pre):
        hFeature = {}
        hFeature['ObjLvl%sNeighborNum' %(pre)] = len(obj.GetNeighbor())
        return hFeature
    
    def ExtractTypeNum(self,qid,query,obj,pre):
        hFeature = {}
        hFeature['ObjLvl%sTypeNum' %(pre)] = len(obj.GetType())
        return hFeature 
    
    def ExtractHasNotable(self,qid,query,obj,pre):
        hFeature = {}
        Notable = obj.GetNotableType()
        score = 0
        if Notable != "":
            score = 1.0
        hFeature['ObjLvl%sHasNotable' %(pre)] = score
        return hFeature
     
         
        
        
        