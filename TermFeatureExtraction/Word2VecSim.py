'''
Created on May 6, 2014
extract word to vec similar feature for query-term
totally different from those features from serp
do:
    read a q-term exp file
    hash all positions of terms.
    go through GoogleNewWord2Vec, record all vec for q,term
    for all q-exp term, calc cosine
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/TermFeatureExtraction')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from cxBase.base import *
from word2vec.WordVecBase import *
from cxBase.Vector import VectorC
import os
import pickle
import ntpath
from copy import deepcopy
import json
from base.ExpTerm import *

class QueryExpTermWord2VecSimFeatureExtractorC(cxBaseC):
    def Init(self):
        self.InName = ""
        self.llExpTerm = []
        self.lVector = [] #corresponding vector for query and terms
        self.hTargetTerm = {}
        self.Word2VecPath = ""
        self.OutName = ""
        
        
    @staticmethod
    def ShowConf():
        print "in\nword2vec\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.InName = conf.GetConf('in')
        self.Word2VecPath = conf.GetConf('word2vec')
        self.OutName = conf.GetConf('out')
        return
    
    
    def LoadAndSetExpTerms(self):
        self.llExpTerm = ReadQExpTerms(self.InName)
        
        #start set 2 invert dict
        for i in range(len(self.llExpTerm)):
            lExpTerm = self.llExpTerm[i]
            for qterm in lExpTerm[0].query.split():
                self.hTargetTerm[qterm] = -1
                
            for j in range(len(lExpTerm)):
                term = lExpTerm[j].term
                self.hTargetTerm[term] = -1
        print "total require [%d] target term" %(len(self.hTargetTerm))
        return True
    
    def LoadVectorForTerm(self):
        WordVecReader = Word2VecReaderC()
        WordVecReader.open(self.Word2VecPath)
        
        for WordVec in WordVecReader:
            if not WordVec.word in self.hTargetTerm:
                continue
            print "read vec for term [%s] to [%d]" %(WordVec.word,len(self.lVector))
            self.hTargetTerm[WordVec.word] = len(self.lVector)
            self.lVector.append(VectorC(WordVec.hDim))
            
            
    def ExtractForOne(self,ExpTerm):
        #calc the ave vector of q terms
        #calc the vector for exp terms
        score = 0
        hFeature = {}
        hFeature['word2vecsim'] = score
        QVector = VectorC()
        TermVector = VectorC()
        QTermCnt = 0
        
        if self.hTargetTerm[ExpTerm.term] == -1:
            print "term [%s] not appear in word2vec" %(ExpTerm.term)
            return hFeature
        
        TermVector = self.lVector[self.hTargetTerm[ExpTerm.term]]
        
        for qterm in ExpTerm.query.split():
            if self.hTargetTerm[qterm] == -1:
                print "qterm [%s] not appear in word2vec" %(qterm)
                continue  
            QTermCnt += 1
            QVector += self.lVector[self.hTargetTerm[qterm]]
        QVector /= float(QTermCnt)
        
        score = VectorC.cosine(QVector,TermVector)
        hFeature['word2vecsim'] = score
        return hFeature
    
    def ExtractFeature(self):
        out = open(self.OutName,'w')
        for i in range(len(self.llExpTerm)):
            for j in range(len(self.llExpterm[i])):
                hFeature = self.ExtractForOne(self.llExpTerm[i][j])
                self.llExpTerm[i][j].AddFeature(hFeature)
                print >>out, self.llExpTerm[i][j].dump()
        out.close()
        return True
    
    def Process(self):
        print "start load and set expterm"
        self.LoadAndSetExpterms()
        print "laod vector from data"
        self.LoadVectorForTerm()
        print "all information get, extracting"
        self.ExtractFeature()
        print "done"
        return True
        
        
            
        
        
        
        
            
            
        

