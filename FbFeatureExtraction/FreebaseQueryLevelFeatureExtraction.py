'''
Created on Jun 10, 2014
query level feature, to describe whether a query should be expansion via our method
features:
    query length
    min query term length
    Facc obj's score, first obj/second obj. if first obj's score is much better than second, it is good.
    First Facc obj name|alias == query
    First Facc obj name|alias part match query (match fraction)
    rank of Facc obj has same name|alias with query
    #facc obj has similiar score (the first drop? 1/3?)
    #facc obj has same name
    # of category of facc results
    
in:
    no additional input. maybe some parameter to set (mostly use default through)
do:
    for each new query meet:
        fill all objects
        extract features
        and set for all terms
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.TextBase import *
from cxBase.Conf import cxConfC
from FbFeatureExtraction.FreebaseFeatureExtraction import *


class FreebaseQueryLevelFeatureExtractionC(FreebaseFeatureExtractionC):
    
    def Init(self):
        self.DropFraction = 3.0/2.0
        self.CurrentQid = -1
        self.hCurrentQFeature = {}
        
        super(FreebaseQueryLevelFeatureExtractionC,self).Init()
        
        
    def SetConf(self,ConfIn):
        super(FreebaseQueryLevelFeatureExtractionC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.DropFraction = conf.GetConf('faccscoredropfraction',self.DropFraction)
        
    @staticmethod
    def ShowConf():
        FreebaseFeatureExtractionC.ShowConf()
        print "faccscoredropfraction"
        
    
    
    
    def ExtractQFeature(self,qid,query):
        if qid == self.CurrentQid:
            return self.hCurrentQFeature
        
        print "start extracting q level [%s][%s]" %(qid,query)
        
        self.CurrentQid = qid
        
        hFeature = {}
        lObj = []
        hFeature.update(self.ExtractQLength(qid,query,lObj))
        
        if qid in self.hQObj:
            lObj = self.hQObj[qid]
            hFeature.update(self.ExtractFaccObjScoreFraction(qid,query,lObj))
            hFeature.update(self.ExtractFaccObjNameAliasMatch(qid,query,lObj))
            hFeature.update(self.ExtractFaccObjNameDuplicate(qid,query,lObj))
            hFeature.update(self.ExtractFaccObjCategoryNum(qid,query,lObj))        
        self.hCurrentQFeature = hFeature
        return self.hCurrentQFeature
    
    
    def ExtractForOneTerm(self,ExpTerm):
        hFeature = self.ExtractQFeature(ExpTerm.qid, ExpTerm.query)
        print "extractin q level for [%s][%s][%s]" %(ExpTerm.qid,ExpTerm.query,ExpTerm.GetName())
        ExpTerm.AddFeature(hFeature)
        return ExpTerm
        

        
        
        
    
    
    def ExtractQLength(self,qid,query,lObj):
        hFeature = {}
        vQTerm = query.split()
        hFeature['QLvlQLen'] = len(vQTerm)
        lQTermLen = [len(term) for term in vQTerm]
        hFeature['QLvlMinQTermLen'] = min(lQTermLen)
        return hFeature
    
    
    def ExtractFaccObjScoreFraction(self,qid,query,lObj):
        hFeature = {}
        if len(lObj) > 1:
            hFeature['QLvlFaccScoreTopSecond'] = lObj[0].GetScore() / lObj[1].GetScore()
            
        #the first > self.DropFraction position
        for i in range(len(lObj) - 1):
            if lObj[i].GetScore() / lObj[i+1].GetScore() >= self.DropFraction:
                hFeature['QLvlFaccScoreFirstDrop'] = i
        if not'QLvlFaccScoreFirstDrop' in hFeature:
            hFeature['QLvlFaccScoreFirstDrop'] = len(lObj)
        return hFeature
    
    
    def ExtractFaccObjNameAliasMatch(self,qid,query,lObj):
        hFeature = {}
        #The rank 1 obj's max((name,alias) overlap with q)
        #The rank of first obj has exactly same name|alias with q
        #the rank of first obj has partial overlap with q
        
        lFirstName = [lObj[0].GetName()] + lObj[0].GetAlias()
        MaxOverlap = 0
        lFirstName = [TextBaseC.RawClean(item) for item in lFirstName]
        
        for name in lFirstName:
            MaxOverlap = max(MaxOverlap,TextBaseC.TermMatchFrac(name,query))
            
        hFeature['QLvlFaccFirstObjNameMatch'] = MaxOverlap
        
        
        flag = False
        for i in range(len(lObj)):
            lName = [lObj[i].GetName()] + lObj[i].GetAlias()
            for name in lName:
                if TextBaseC.RawClean(name) == TextBaseC.RawClean(query):
                    hFeature['QLvlFaccFirstSameQueryObjRank'] = i
                    flag = True
                    break
            if flag:
                break
        if not flag:
            hFeature['QLvlFaccFirstSameQueryObjRank'] = len(lObj)
            
            
        flag = False
        for i in range(len(lObj)):
            lName = [lObj[i].GetName()] + lObj[i].GetAlias()
            for name in lName:
                if TextBaseC.RawClean(name) in TextBaseC.RawClean(query):
                    hFeature['QLvlFaccFirstInQueryObjRank'] = i
                    flag = True
                    break
            if flag:
                break
        if not flag:
            hFeature['QLvlFaccFirstInQueryObjRank'] = len(lObj)                

        return hFeature
    
    def ExtractFaccObjNameDuplicate(self,qid,query,lObj):
        hFeature = {}
        #get all names, sort and count for the most duplicated one.
        #not using alias june 10
        
        hName = {}
        
        for obj in lObj:
            name = obj.GetName()
            if name == "":
                continue
            if not name in hName:
                hName[name] = 1
            else:
                hName[name] += 1
        
        lCnt = [cnt for name,cnt in hName.items()]
        hFeature['QLvlFaccNameDuplicate'] = max(lCnt)
        return hFeature
    
    
    def ExtractFaccObjCategoryNum(self,qid,query,lObj):
        hFeature = {}
        #get all categories. except common, user, etc
        
        hType = {}
        for obj in lObj:
            lType = obj.GetType(Filter=True)
            hType.update(zip(lType,[True] * len(lType)))
        
        hFeature['QLvlFaccObjTypeCnt'] = len(hType)     
        return hFeature

        
        
        
        
        
        
    