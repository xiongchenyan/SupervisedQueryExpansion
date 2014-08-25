'''
Created on Aug 22, 2014
evaluate the performance of individual objects in expansion
the performance is by using single object's prf
in: expansion required part + re-ranking required part + evaluation required part + objs
out: q-obj-ground truth score
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from IndriRelate.IndriInferencer import *
from IndriRelate.IndriPackedRes import *
from AdhocEva.AdhocEva import *
from AdhocEva.AdhocQRel import *
from ExpansionReranker.WeightedReRanker  import WeightedReRankerC
from base.ExpTerm import *
from PrfFreebaseExpansion.FreebaseObjRankExpansion import *

class ObjLabelViaDocRankingScoreC(cxBaseC):
    def Init(self):
        self.InName = ""
        self.OutName = ""
        self.CashDir = ""
        self.RelCenter = AdhocQRelC()
        self.NewTermW = 0.1
        self.ReRankDepth = 100
        self.ReRanker = WeightedReRankerC()
        self.DFMin = 0
        self.Expander = FreebaseObjRankExpansionC()
        
    @staticmethod
    def ShowConf():
        print "in\nout\ncashdir\nrerankdepth\nqrel\n"
        WeightedReRankerC.ShowConf()
        FreebaseObjRankExpansionC.ShowConf()

    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        self.CashDir = conf.GetConf('cashdir')
        self.RelCenter.Load(conf.GetConf('qrel'))
        self.ReRanker.SetConf(ConfIn)
        self.NewTermW = float(conf.GetConf('newtermweight',self.NewTermW))
        self.ReRankDepth = int(conf.GetConf('rerankdepth',self.ReRankDepth))
        self.DFMin = int(conf.GetConf('dfmin',self.DFMin))
        self.Expander.SetConf(ConfIn)
        
        
    def EvaPerObj(self,qid,query,ObjId,lDoc):
        '''
        1, call expander get exp terms
        2, rerank
        3, compare ranking score, get final performance gain 
        '''
        
        lExpTerm = self.Expander.ExpandUsingOneObj(qid, query, ObjId, lDoc)
        lReRankDoc = self.ReRanker.ReRank(lDoc, lExpTerm)        
        return self.CalcInfluenceScore(qid, lReRankDoc, lDoc)
        
    
    def Process(self):
        '''
        read q-obj rank from InName
        call EvaPerObj
        output q-obj score in the last column, to output
        '''
        out  = open(self.OutName,'w')
        lDoc = []
        ThisQId = ""
        for line in open(self.InName):
            line = line.strip()
            vCol = line.split('\t')
            qid,query,ObjId = vCol[:3]
            if qid != ThisQId:
                lDoc = ReadPackedIndriRes(self.CashDir + '/' + query)
                print "loaded docs for [%s]" %(qid)
                ThisQId = qid
            print "evaluating [%s][%s][%s]" %(qid,query,ObjId)            
            InfluenceScore = self.EvaPerObj(qid, query, ObjId, lDoc)
            print >>out,line + '\t%f' %(InfluenceScore)
        out.close()
        print "finished" 
    
        
        
        
    def CalcInfluenceScore(self,qid, lReRankDoc,lDoc):
        hBaseDocScore = {}
        for doc in lDoc:
            hBaseDocScore[doc.DocNo] = doc.score
            
        RelGain = 0
        RelCnt = 0
        NoiseGain = 0
        NoiseCnt = 0
        
        for doc in lReRankDoc:
            ScoreChange = doc.score - hBaseDocScore[doc.DocNo]
            Rel = self.RelCenter.GetScore(qid, doc.DocNo)
            if Rel > 0:
                RelGain += ScoreChange
                RelCnt += 1
            else:
                NoiseGain += ScoreChange
                NoiseCnt += 1
                
        if RelCnt != 0:
            RelGain /= RelCnt
        if NoiseCnt != 0:
            NoiseGain /= NoiseCnt
            
        return RelGain - NoiseGain
