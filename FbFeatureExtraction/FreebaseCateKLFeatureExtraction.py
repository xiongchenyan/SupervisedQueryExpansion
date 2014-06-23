'''
Created on Jun 23, 2014
extract KL divergence feature between query and term
SetConf: load nb classifier
in prepare:
    calc the query's P(cate|q), and put in vector
for each term:
    calc term's P(cate|term), and put in vector
    calc KL via vector's API
@author: chenyan
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from FbFeatureExtraction.FreebaseFeatureExtraction import *

from cxBase.TextBase import *
from cxBase.Vector import *
from TextClassification.NaiveBayesianClassifier import *


class FreebaseCateKLFeatureExtractionC(FreebaseFeatureExtractionC):
    
    def Init(self):
        super(FreebaseCateKLFeatureExtractionC,self).Init()
        self.QCateVector = VectorC()
        self.NbCenter = NaiveBayesianClassifierC()
        
    def SetConf(self,ConfIn):
        super(FreebaseCateKLFeatureExtractionC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.NbCenter.load(conf.GetConf('nbclassifierdump'))
        
        
    @staticmethod
    def ShowConf():
        FreebaseFeatureExtractionC.ShowConf()
        print "nbclassifierdump"
    
    
    def ExtractForOneTerm(self,ExpTerm):
        #no relationship with object rank, just using Freebase's category Nb classifier
        
        lProb = self.NbCenter.Predict(ExpTerm.term)[1]
        TermVec = VectorC(lProb)
        
        ExpTerm = self.ExtractQTermKL(ExpTerm,TermVec)
        
        return ExpTerm
    
    
    def ExtractQTermKL(self,ExpTerm,TermVec):
        score = VectorC.TwoWayKL(self.QCateVector, TermVec)
        ExpTerm.hFeature['QTermCateKL'] = score
        return ExpTerm
    
    
    def Prepare(self,qid,query):
        lProb = self.NbCenter.Predict(query)[1]
        self.QCateVector = VectorC(lProb)
        return True