'''
Created on Mar 18, 2014
full pipe from query => exp terms, features, scores
now only using infor from SERP
@author: cx
'''

'''
4/23/2014
update to allow input in each step

'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from CandidateTermGeneration.CandidateTermFromSERP import *
from TermLabel.SingleTermPerformance import *
from TermLabel.TermLabelViaDocRankingScore import *
from TermFeatureExtraction.SERPFeatureExtractFull import *
from cxBase.KeyFileReader import KeyFileReaderC
import json
from cxBase.base import cxConf,cxBaseC
class TrainingDataFromSERPC(cxBaseC):
    
    def Init(self):
        self.OutFormat = 'normal' #or svm?
        self.CashDir = ""
        self.TotalDocToRead = 1000
        self.CandidateTermGetter = CandidateTermFromSERPC()
        self.TermLabelGetter = TermLabelViaDocRankingScoreC()
        self.FeatureExtractor = SERPFeatureExtractFullC()
        
        self.GenerateTerm = True
        self.LabelTerm = True
        self.ExtractPRFFeature = True
        
        return
    
    @staticmethod
    def ShowConf():
        print "totalserpnum 1000\ncashdir\nminfiltercnt 3"
        print "numofserpdoc 20\nbgdocnum 100\nctf\noutformat normal"
        print "generateterm 1\nlabelterm 1 extractprffeature 1"
        TermLabelViaDocRankingScoreC.ShowConf()
    def SetConf(self,ConfIn):
       
        
        self.CandidateTermGetter.SetConf(ConfIn)
        self.TermLabelGetter.SetConf(ConfIn)
        self.FeatureExtractor.SetConf(ConfIn)
        conf  = cxConf(ConfIn)
        self.OutFormat = conf.GetConf('outformat')
        self.TotalDocToRead = conf.GetConf('totalserpnum')
        self.CashDir = conf.GetConf('cashdir')
        
        self.GenerateTerm = bool(int(conf.GetConf('generateterm',1)))
        self.LabelTerm = bool(int(conf.GetConf('labelterm',1)))
        self.ExtractPRFFeature = bool(int(conf.GetConf('extractprffeature',1)))
        return True
    
            
            
    def ProcessOneQuery(self,qid,query,lExpTerm):
        lDoc = ReadPackedIndriRes(self.CashDir + '/' + query,self.TotalDocToRead)
        
        lTerm = []
        if (lExpTerm == []) | (self.GenerateTerm):
            lTerm = self.CandidateTermGetter.Process(query, lDoc)
            print "q [%s] get [%d] candidate term" %(query,len(lTerm))
            print json.dumps(lTerm,indent=1)
            
            for term in lTerm:
                ExpTerm = ExpTermC()
                ExpTerm.qid = qid
                ExpTerm.query = query
                ExpTerm.term = term
                lExpTerm.append(ExpTerm)
        else:
            lTerm = [ExpTerm.term for ExpTerm in lExpTerm]
            
        if self.LabelTerm:    
            lScore = self.TermLabelGetter.EvaluatePerQ(qid, query, lTerm, lDoc)
            for i in range(len(lScore)):
                lExpTerm[i].score = lScore[i]
        
        if self.ExtractPRFFeature:
            self.FeatureExtractor.Process(lExpTerm, lDoc)
        return lExpTerm
    
    
    
    def SegLoadData(self,lvCol):
        qid = lvCol[0][0]
        query = lvCol[0][1]
        lExpTerm = []
        if not self.GenerateTerm:
            #input type is exp term
            for vCol in lvCol:
                ExpTerm = ExpTermC('\t'.join(vCol))
                lExpTerm.append(ExpTerm)
        return qid,query,lExpTerm
    
    
    
    def Process(self,InName,OutName):
        out = open(OutName,'w')
        
        KeyReader = KeyFileReaderC()
        
        KeyReader.open(InName)
        
        
        for lvCol in KeyReader:
            qid,query,lExpTerm = self.SegLoadData(lvCol)
            lExpTerm = self.ProcessOneQuery(qid, query,lExpTerm)
            for ExpTerm in lExpTerm:
                if self.OutFormat == 'normal':
                    print >>out,ExpTerm.dump()
                else:
                    print "not implemented yet"
        out.close()
        return True
        
        
        
        
    
    
    