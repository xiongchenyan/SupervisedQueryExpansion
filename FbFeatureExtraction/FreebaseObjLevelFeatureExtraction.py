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
        self.lObjLm = []
        self.ThisQid = -1
        self.lObjFeature = []
        super(FreebaseObjLevelFeatureExtractionC,self).Init()
    
    def CalcObjLm(self,lObj):
        del self.lObjLm[:]
        
        for obj in lObj:
            desp = obj.GetDesp()
            Lm = LmBaseC(desp)
            for term in Lm.hTermTF:
                score = Lm.GetTFProb(term) * self.CtfCenter.GetLogIdf(term)
                Lm.hTermTF[term] = score
            Lm.CalcLen()
            self.lObjLm.append(Lm)
        return   
    
    
    def CalcTermObjScore(self,term):
        lObjScore = [1.0/len(self.lObjLm)] * len(self.lObjLm)
        
        lObjProb = [Lm.GetTFProb(term) for Lm in self.lObjLm]
        Total = float(sum(lObjProb))
        if 0 != Total:
            lObjScore = [pTermObj / Total for pTermObj in lObjProb]
        return lObjScore
    
    
    def ExtractForOneTerm(self,ExpTerm):
        if not ExpTerm.qid in self.hQObj:
            return ExpTerm
        lObj = self.hQObj[ExpTerm.qid]
        self.ExtractObjFeatureAndCalcObjLm(ExpTerm.qid, ExpTerm.query, lObj)
        
        print "extracting ObjLvl for [%s][%s][%s]" %(ExpTerm.qid,ExpTerm.query,ExpTerm.term)
        lObjScore = self.CalcTermObjScore(ExpTerm.term)
        print "term obj p:%s" %(json.dumps(lObjScore))
        FeatureVector = VectorC()
        for i in range(len(lObjScore)):
            FeatureVector += self.lObjFeature[i] * lObjScore[i]
        
        ExpTerm.AddFeature(FeatureVector.hDim)
        
        return ExpTerm
        
        
    
        
    def ExtractObjFeatureAndCalcObjLm(self,qid,query,lObj):
        
        if qid == self.ThisQid:
            return
        print "preparing obj feature for query [%s][%s]" %(qid,query)
        self.CalcObjLm(lObj)
        
        del self.lObjFeature[:]
        self.ThisQid = qid
        
        for obj in lObj:
            FeatureVector = self.ExtractForOneObj(qid,query,obj)
            self.lObjFeature.append(FeatureVector)        
        return 

    def ExtractForOneObj(self,qid,query,obj):
        FeatureVector = VectorC()
        print "extracting obj feature for [%s][%s][%s]" %(qid,query,obj.GetName())
        FeatureVector.hDim.update(self.ExtractFaccScore(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractLmScore(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractNameEqual(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractQInDespFrac(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractNeighborNum(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractTypeNum(qid,query,obj))
        FeatureVector.hDim.update(self.ExtractHasNotable(qid,query,obj))
        
        return FeatureVector
        
    
    def ExtractFaccScore(self,qid,query,obj):
        hFeature = {}
        hFeature['ObjLvlFaccScore'] = obj.GetScore()
        return hFeature
    
    
    
    
    def ExtractLmScore(self,qid,query,obj):
        hFeature = {}
        NameLm = LmBaseC(obj.GetName())
        DespLm = LmBaseC(obj.GetDesp())
        Inferencer = LmInferencerC()
        score = 0.5 * Inferencer.InferQuery(query, NameLm, self.CtfCenter)
        score += 0.5 * Inferencer.InferQuery(query,DespLm,self.CtfCenter)
        hFeature['ObjLvlLmScore'] = score
        return hFeature
    
    def ExtractNameEqual(self,qid,query,obj):
        hFeature = {}
        
        lName = [obj.GetName()] + obj.GetAlias()
        lName = [TextBaseC.RawClean(text) for text in lName]
        score = 0
        target = TextBaseC.RawClean(query)
        if target in lName:
            score = 1.0
        hFeature['ObjLvlNameEqualQuery'] = score
        return hFeature    
    
    def ExtractQInDespFrac(self,qid,query,obj):
        hFeature = {}
        
        desp = TextBaseC.RawClean(obj.GetDesp())
        lQTerm =  TextBaseC.RawClean(query).split()
        score = 0
        for term in lQTerm:
            if term in desp:
                score += 1
        hFeature['ObjLvlQInDespFrac'] = score / len(lQTerm)
        return hFeature 
    
    def ExtractNeighborNum(self,qid,query,obj):
        hFeature = {}
        hFeature['ObjLvlNeighborNum'] = len(obj.GetNeighbor())
        return hFeature
    
    def ExtractTypeNum(self,qid,query,obj):
        hFeature = {}
        hFeature['ObjLvlTypeNum'] = len(obj.GetType())
        return hFeature 
    
    def ExtractHasNotable(self,qid,query,obj):
        hFeature = {}
        Notable = obj.GetNotableType()
        score = 0
        if Notable != "":
            score = 1.0
        hFeature['ObjLvlHasNotable'] = score
        return hFeature
     
         
        
        
        