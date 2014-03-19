'''
Created on Mar 18, 2014
full pipe from query => exp terms, features, scores
now only using infor from SERP
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from CandidateTermGeneration.CandidateTermFromSERP import *
from TermLabel.SingleTermPerformance import *
from TermFeatureExtraction.SERPFeatureExtractFull import *

import json

class TrainingDataFromSERPC(object):
    
    def Init(self):
        self.OutFormat = 'normal' #or svm?
        self.CashDir = ""
        self.TotalDocToRead = 1000
        self.CandidateTermGetter = CandidateTermFromSERPC()
        self.TermLabelGetter = SingleTermPerformanceC()
        self.FeatureExtractor = SERPFeatureExtractFullC()
        return
    
    
    def SetConf(self,ConfIn):
        print "conf:\ntotalserpnum 1000\ncashdir\nminfiltercnt 3"
        print "newtermweight 0.01\nusebinaryscore 0\nnumofserpdoc 20\nbgdocnum 100\nctf\noutformat normal"
        
        
        self.CandidateTermGetter.SetConf(ConfIn)
        self.TermLabelGetter.SetConf(ConfIn)
        self.FeatureExtractor.SetConf(ConfIn)
        conf  = cxConf(ConfIn)
        self.OutFormat = conf.GetConf('outformat')
        self.TotalDocToRead = conf.GetConf('totalserpnum')
        self.CashDir = conf.GetConf('cashdir')
        return True
    
    def __init__(self,ConfIn=""):
        self.Init()
        if ConfIn != "":
            self.SetConf(ConfIn)
            
            
    def ProcessOneQuery(self,qid,query):
        lDoc = ReadPackedIndriRes(self.CashDir + '/' + query,self.TotalDocToRead)
        lExpTerm = []
        lTerm = self.CandidateTermGetter.Process(query, lDoc)
        
        print "q [%s] get [%d] candidate term" %(query,len(lTerm))
        print json.dumps(lTerm,indent=1)
        
        for term in lTerm:
            ExpTerm = ExpTermC()
            ExpTerm.qid = qid
            ExpTerm.query = query
            ExpTerm.term = term
            lExpTerm.append(ExpTerm)
        lScore = self.TermLabelGetter.EvaluatePerQ(qid, query, lTerm, lDoc)
        for i in range(len(lScore)):
            lExpTerm[i].score = lScore[i]
        
        self.FeatureExtractor.Process(lExpTerm, lDoc)
        return lExpTerm
    
    
    def Process(self,QInName,OutName):
        out = open(OutName,'w')
        for line in open(QInName):
            qid,query = line.strip().split('\t')
            lExpTerm = self.ProcessOneQuery(qid, query)
            for ExpTerm in lExpTerm:
                if self.OutFormat == 'normal':
                    print >>out,ExpTerm.dump()
                else:
                    print "not implemented yet"
        out.close()
        return True
        
        
        
        
    
    
    