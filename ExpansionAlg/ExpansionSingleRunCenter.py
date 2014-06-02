'''
Created on Apr 1, 2014
the cleaner version of ExpansionSingleRunPipe
@author: cx

changed:
1, only apply to one input data + one set of para, cv of para is done by condor submiter
2, in output expansion term, support more depth
3, add load base data in class, by conf 

'''

import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import *
from IndriRelate.IndriPackedRes import *
from operator import attrgetter
from base.ExpTerm import *
from CrossValidation.ParameterSet import *
from AdhocEva.AdhocEva import *
from AdhocEva.AdhocMeasure import *
from IndriExpansionBaseline.IndriExpansion import *
from ExpansionReranker.WeightedReRanker import *
from MixtureModelExpansion.MixtureModelExpansion import *
from ScoreMergeExpansion import *
from PrfFreebaseExpansion.FreebaseObjRankExpansion import *
import os,json

class ExpansionSingleRunCenterC(cxBaseC):
    
    def Init(self):
        self.CashDir = ""
        self.QueryIn = ""
        self.EvaOutDir = ""
        self.CtfPath = ""
        self.ConfIn = ""
        self.ParaSet = ParameterSetC()
        self.NumOfReRankDoc = 100
        self.ExpansionMethod = 'merge'
        self.InputType = 'qterm'
        self.OutExpTerm = False
        self.MaxExpTermToKeep = 1000
        self.NumOfExpTerm = 10
        
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.ConfIn = ConfIn
        self.CashDir = conf.GetConf("cashdir")
        self.ExpDocCashDir = conf.GetConf('expcashdir',self.CashDir)
        self.QueryIn = conf.GetConf('in')
        self.EvaOutDir = conf.GetConf('evaoutdir')
        self.CtfPath = conf.GetConf('ctfpath')
        self.NumOfReRankDoc = int(conf.GetConf('rerankdepth',self.NumOfReRankDoc))        
        self.ExpansionMethod = conf.GetConf('expmethod',self.ExpansionMethod)
        self.InputType = conf.GetConf('inputtype',self.InputType)
        self.OutExpTerm  = bool(int(conf.GetConf('outexpterm',0)))
        self.NumOfExpTerm = int(conf.GetConf('numofexpterm',self.NumOfExpTerm))
        if not os.path.exists(self.EvaOutDir):
            os.makedirs(self.EvaOutDir)
        self.ParaSet = ReadParaSet(conf.GetConf('paraset'))[0]
        return True
    
    
    @staticmethod
    def ShowConf():
        print "cashdir\nin\nevaoutdir\nctfpath"
        print "rerankdepth\nparaset\nexpmethod rm|mix|merge|fbprf"
        print "inputtype qterm|query\noutexpterm 0"        
        ScoreMergeExpansionC.ShowConf()
        IndriExpansionC.ShowConf()
        MixtureModelExpansionC.ShowConf()
        WeightedReRankerC.ShowConf()
        AdhocEvaC.ShowConf()
        return True
    
    def ProcessPerQ(self,qid,query):
        #load ldocs
        #for each para
            #call process for one para
            #record performance
        #return llEvaRes, the performance of this qid at all paras                
        lDoc = ReadPackedIndriRes(self.CashDir + '/' + query,self.NumOfReRankDoc)    
        lExpDoc = ReadPackedIndriRes(self.ExpDocCashDir + '/' + query,self.NumOfReRankDoc)     
        ExpansionCenter = QueryExpansionC()
        if self.ExpansionMethod == 'rm':
            ExpansionCenter = IndriExpansionC(self.ConfIn)
        if self.ExpansionMethod == 'mix':
            ExpansionCenter = MixtureModelExpansionC(self.ConfIn)  
        if self.ExpansionMethod == 'merge':
            ExpansionCenter = ScoreMergeExpansionC(self.ConfIn)   
        if self.ExpansionMethod == 'fbprf':
            ExpansionCenter = FreebaseObjRankExpansionC(self.ConfIn)
            
             
        WeightedReRanker = WeightedReRankerC(self.ConfIn)
        AdhocEva = AdhocEvaC(self.ConfIn)
        
        ExpansionCenter.SetParameter(self.ParaSet)
        WeightedReRanker.SetParameter(self.ParaSet)
        #AdhocEva not parameter to switch
        self.SetParameter(self.ParaSet)
        print "start run [%s][%s]" %(qid,query)
        ExpansionCenter.NumOfExpTerm = self.MaxExpTermToKeep
        #expand
        lExpTerm = ExpansionCenter.Process(qid, query, lExpDoc)
        print "exp done get [%d] exp term" %(len(lExpTerm))
        #reranking
        lReRankedDoc = WeightedReRanker.ReRank(lDoc, list(lExpTerm[:self.NumOfExpTerm]))
        print "re ranking done"
        #evaluation
        EvaMeasure = AdhocEva.EvaluatePerQ(qid, AdhocEva.SegDocNoFromDocs(lReRankedDoc))
        print "eva done"
        return EvaMeasure,lExpTerm      
    
    
    def SetParameter(self,ParaSet):
        if "numofexpterm" in ParaSet.hPara:
            self.NumOfExpTerm = int(ParaSet.hPara['numofexpterm'])
        return True 
    
    def LoadData(self):
        lQidQuery = []
        if self.InputType == 'qterm':
            for line in open(self.QueryIn):
                QTerm = ExpTermC(line.strip())
                lQidQuery.append(QTerm.qid +"_"+QTerm.query)
                lQidQuery = list(set(lQidQuery)) 
            for i in range(len(lQidQuery)):
                lQidQuery[i] = lQidQuery[i].split('_')
            return lQidQuery           
        if self.InputType == 'query':
            for line in open(self.QueryIn):
                qid,query = line.strip().split('\t')
                lQidQuery.append([qid,query])      
            return lQidQuery
        print "input type [%s] not recognized" %(self.InputType)
        return []
    
    
    def Process(self):
        
        lEvaRes = []
        lQid = []
        lQuery = []
        lQidQuery = self.LoadData()
        lExpTerm = [] #dim0:query, dim1: para, dim2: terms
        for qid,query in lQidQuery:
            lQid.append(qid)
            lQuery.append(query)
            EvaRes,lMidExpTerm = self.ProcessPerQ(qid, query)
            lExpTerm.extend(lMidExpTerm)
            lEvaRes.append(EvaRes)            
        print "runs finished, wrap up evaluation results"
        self.DumpPerQRes(lQid,lEvaRes)
        self.DumpMean(lEvaRes)
        if self.OutExpTerm:
            self.DumpExpTerm(lExpTerm)       
        print "finished"
        return True
    
     
    def DumpExpTerm(self,lExpTerm):
        out = open(self.EvaOutDir + "/ExpTerm",'w')
        for ExpTerm in lExpTerm:
            print >>out, ExpTerm.dump()
        out.close()            
        return True
                                  
        
        
    
    
    def DumpPerQRes(self,lQid,lEvaRes):
        out = open(self.EvaOutDir + "/PerQEva",'w')
        for QIndex in range(len(lQid)):
            EvaRes = lEvaRes[QIndex]
            qid = lQid[QIndex]            
            print >> out,"%s\t%s" %(qid,EvaRes.dumps())
        
        EvaMean = AdhocMeasureMean(lEvaRes)
        print >> out,"mean\t%s" %(EvaMean.dumps())
        out.close()              
        return True
    
    def DumpMean(self,lEvaRes):   
        out = open(self.EvaOutDir + "/MeanVsPara",'w')
        EvaMean = AdhocMeasureMean(lEvaRes)
        print >> out,"mean\t%s" %(EvaMean.dumps())    
        out.close()        
        return True
        
        
        
    
