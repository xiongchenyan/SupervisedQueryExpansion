'''
Created on Mar 24, 2014
input: model ParaSet K(if need turn para), expterms (with label)
baseline exp term(to merge score)
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')

from LibSVMRelate.SVMBase import *
from svmutil import *
from CrossValidation.ParameterSet import *
from CrossValidation.RandomSplit import *
from cxBase.base import *
from base.ExpTerm import *
from AdhocEva.AdhocEva import *
from AdhocEva.AdhocMeasure import *
from IndriRelate.IndriInferencer import *
from IndriRelate.IndriPackedRes import *
from ExpansionReranker.WeightedReRanker import *
from operator import itemgetter
import os,json

class SVMModelTestC(object):
    def Init(self):
        self.Alpha = 0.5
        self.ReRankDepth = 1000
        self.ConfIn = ""
        self.CashDir = ""
        self.lBaseExpTerm = []
        self.hBaseExpTerm = {} #index
        self.CVOptMeasure = 'err'
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.ConfIn = ConfIn
        self.Alpha = float(conf.GetConf('alpha'))
        self.ReRankDepth = int(conf.GetConf('rerankdepth'))
        self.CashDir = conf.GetConf('cashdir')
        llExpTerm = ReadQExpTerms(conf.GetConf('baselineterm'))
        for lExpTerm in llExpTerm:
            self.lBaseExpTerm.extent(lExpTerm) 
        return True
    
    def SetParameter(self,ParaSet):
        if 'alpha' in ParaSet.hPara:
            self.Alpha = float(ParaSet.hPara['alpha'])
        if 'rerankdepth' in ParaSet.hPara:
            self.ReRankDepth = ParaSet.hPara['rerankdepth']
        return True
    
    
    @staticmethod
    def ShowConf():
        print "alpha\nrerankdepth 1000\cashdir"
        
    
    def __init__(self,ConfIn = ''):
        self.Init()
        if '' != ConfIn:
            self.SetConf(ConfIn)
        return True
    
    
    
    
    
    def PredictProb(self,llExpTerm,SVMModel):
        lScore,lhFeature = SplitLabelAndFeature(llExpTerm)
        p_label,p_acc,p_val = svm_predict(lScore,lhFeature,SVMModel,'-b 1')
        print "prediction label:%s\nprob:\n%s" %(json.dumps(p_label,indent=1),json.dumps(p_val,indent=1))
        print "accuracy:%s" %(json.dumps(p_acc))
        
        index = 0
        for i in range(len(llExpTerm)):
            for j in range(llExpTerm[j]):
                llExpTerm[i][j].score = p_val[index][1] #prob of being class 1 #need check index of labels
                index += 1        
        return llExpTerm
        
        
   
    def MergeWithBaseScore(self,lExpTerm):
        #for one query
        Z= 0
        lResTerm = []
        self.BuildhBaseExpTerm()
        for ExpTerm in lExpTerm:
            key = ExpTerm.Key()
            BaseScore = 0
            if key in self.hBaseExpTerm:
                BaseScore = self.lBaseExpTerm[self.hBaseExpTerm[key]].score
            ThisScore = BaseScore * (1 + self.Alpha * ExpTerm.score)
            Z += ThisScore
            lResTerm.append(copy.deepcopy(ExpTerm))
            lResTerm[len(lResTerm) - 1].score = ThisScore        
        
        if 0 != Z:
            for i in range(len(lResTerm)):
                lResTerm[i].score /= Z        
        return lResTerm
        
        
    
    def BuildhBaseExpTerm(self):
        if {} == self.hBaseExpTerm:
            for i in range(len(self.lBaseExpTerm)):
                self.hBaseExpTerm[self.lBaseExpTerm[i].Key()] = i
        return True
    
    
    def SingleQueryPerParaTest(self,qid,lExpTerm,ParaSet,lDoc):
        #evaluate the performance of lExpTerm, ParaSet, and lDoc
        lResTerm = self.MergeWithBaseScore(lExpTerm)        
        WeightedReRanker = WeightedReRankerC(self.ConfIn)
        AdhocEva = AdhocEvaC(self.ConfIn)  
        WeightedReRanker.SetParameter(ParaSet)
        
        lReRankedDoc = WeightedReRanker.ReRank(lDoc, lResTerm)
        print "re ranking done"
        #evaluation
        EvaMeasure = AdhocEva.EvaluatePerQ(qid, AdhocEva.SegDocNoFromDocs(lReRankedDoc))
        print "eva done"
        
        
        return EvaMeasure
    
    
    
    def SingleQueryTest(self,qid,query,lExpTerm,lParaSet,lDoc=[]):
        if len(lDoc) < self.ReRankDepth:
            lDoc = ReadPackedIndriRes(self.CashDir + '/' + 'query')
        
        llEvaMeasure = [[]]
        for ParaSet in lParaSet:
            llEvaMeasure[0].append(self.SingleQueryPerParaTest(qid,lExpTerm,ParaSet,lDoc))
        return llEvaMeasure
    
    
    
    
    def OneParaRun(self,lQid,lQuery,llExpTerm,ParaSet):
        #if only have one input para set, then run and return the per query measure
        #the score in llExpTerm is predicted by PredictProb
        llEvaMeasure = [] #[query][para]
        for i in range(len(lQid)):
            qid = lQid[i]
            query = lQuery[i]
            llEvaMeasure.extend(self.SingleQueryTest(qid,query,llExpTerm[i],[ParaSet]))
        return llEvaMeasure
            
        
    
    def TestBestReRankPara(self,lQid,lQuery,llExpTerm,lParaSet):
        BestP = 0
        #build llMeasure Matrix by calling SingleQueryTest
        #select the parameter with best performance overrall query
        llEvaMeasure = []
        for i in range(len(lQid)):
            llEvaMeasure.extend(self.SingleQueryTest(lQid[i], lQuery[i], llExpTerm[i], lParaSet))
        
        lPerParaMeanMeasure = AdhocMeasureMatrixMean(llEvaMeasure)
        
        BestP = GetBestPerform(lPerParaMeanMeasure,self.CVOptMeasure)  
        
        return lParaSet[BestP]
    
    def Test(self,lQid,lQuery,llExpTerm,lParaSet,SVMModel, K=5):
        llExpTerm = self.PredictProb(llExpTerm, SVMModel)
        if len(lParaSet) == 1:
            return self.OneParaRun(lQid,lQuery,llExpTerm,lParaSet[0])
        
        llSplit =RandomSplit(llExpTerm,K)
        lPartitionedQid = []
        lPartitionedQuery = []
        llFinalEvaMeasure = []
        for llTrainExpTerm,llTestExpTerm in llSplit:
            ParaSet = self.TestBestReRankPara(lQid, lQuery, llTrainExpTerm, lParaSet)
            lTestQid,lTestQuery = SplitQidQuery(llTestExpTerm)
            llEvaMeasure = self.OneParaRun(lTestQid,lTestQuery,llTestExpTerm,ParaSet)
            lPartitionedQid.extend(lTestQid)
            lPartitionedQuery.extend(lTestQuery)
            llFinalEvaMeasure.extend(llEvaMeasure)
            
        #recover order
        return self.RecoverQidEvaOrder(lQid, lPartitionedQid, llFinalEvaMeasure)
        
        
        
    def RecoverQidEvaOrder(self,lTargetQid,lPartitionedQid,llEvaMeasure):
        hQid = {}
        for i in range(len(lTargetQid)):
            hQid[lTargetQid[i]] = i
        
        lMid = []
        for i in range(len(lPartitionedQid)):
            lMid.append([hQid[lPartitionedQid[i]],llEvaMeasure[i]])            
        lMid.sort(key=itemgetter(0))
        llNewMeasure = [lMeasure for p,lMeasure in lMid]               
        return llNewMeasure    
         
                    
        
 

def SVMModelUnitTest(ConfIn):
    
    print "in\nparaset\nsvmmodel\nk"
    SVMModelTestC.ShowConf()
    
    conf = cxConf(ConfIn)
    ExpTermIn = conf.GetConf('in')
    ParaSetIn = conf.GetConf('paraset')
    SVMModelInName = conf.GetConf('svmmodel')
    K = int(conf.GetConf('k'))
    OutName = conf.GetConf('out')
    SVMTestCenter = SVMModelTestC(ConfIn)  
    
    SVMModel = svm_load_model(SVMModelInName)
    
    llExpTerm = ReadQExpTerms(ExpTermIn)
    lQid,lQuery = SplitQidQuery(llExpTerm)
    lParaSet = ReadParaSet(ParaSetIn)    
    
    llEvaMeasure = SVMTestCenter.Test(lQid,lQuery,llExpTerm,lParaSet,SVMModel,K)
    
    
    
    out = open(OutName,'w')
    for i in range(len(lQid)):
        print >>out,"%s\t%s" %(lQid[i],llEvaMeasure[i][0])
    out.close()
    
    print "finished"
    return True
    
    
    
         
        
        
        
        
        
        
        
        
        
        
            
