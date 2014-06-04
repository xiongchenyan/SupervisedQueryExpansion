'''
Created on Jun 4, 2014
evaluate the expansion term label via document ranking score change
term label = 1/|rel|\sum_i\in rel score(d_i,q+expterm) - score(d_i,q) 
- 1/|irel|\sum_i\in irel score(d_i,q+expterm) - score(d_i,q)


in: q, cash doc, exp terms, qrel
do: 
for each q
    get ranking score of original query
    for each exp term
        get ranking score of expanded query
        calc average relevant document score gain - irrelevant document score gain.
        output
        
done
@author: cx
'''
'''
Key problem:
1: gap between: individual effectiveness -> group effectiveness
2: gap between: ranking score change -> evaluation measure change
3: random influence of terms
'''

'''
for p3:
    set all term that df < 2's score to zero? 
        cause it is highly random and bring noise to label?

'''


import site
site.addsitedir('/bos/usr0/cx/cxPylib')
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


class TermLabelViaDocRankingScoreC(cxBaseC):
    
    def Init(self):
        self.InName = ""
        self.OutName = ""
        self.CashDir = ""
        self.RelCenter = AdhocQRelC()
        self.NewTermW = 0.1
        self.ReRankDepth = 100
        self.ReRanker = WeightedReRankerC()
        self.DFMin = 0
        
    @staticmethod
    def ShowConf():
        print "in\nout\ncashdir\nnewtermweight\nrerankdepth\nqrel\ndfmin"
        WeightedReRankerC.ShowConf()

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
        
    
    
    
    def CalcTermDF(self,term,lDoc):
        DF = 0
        for doc in lDoc:
            if doc.ContainTerm(term):
                DF += 1
        return DF
    
    
        
    def EvaluatePerTerm(self,ExpTerm,lDoc):
        #lDoc contains raw document score already
        
        if self.DFMin > 0:
            DF = self.CalcTermDF(ExpTerm.term, lDoc) 
            if DF < self.DFMin:
                print "term [%s] df [%d] filtered" %(ExpTerm.term, DF)
                return 0.0
            else:
                print "term [%s] df [%d] keep" %(ExpTerm.term, DF)
        
        
        ExpTerm.score = self.NewTermW
        
        lExpTerm = [ExpTerm]
        
        lReRankDoc = self.ReRanker.ReRank(lDoc, lExpTerm)
        
        hBaseDocScore = {}
        for doc in lDoc:
            hBaseDocScore[doc.DocNo] = doc.score
            
            
        RelGain = 0
        RelCnt = 0
        NoiseGain = 0
        NoiseCnt = 0
        
        for doc in lReRankDoc:
            ScoreChange = doc.score - hBaseDocScore[doc.DocNo]
            Rel = self.RelCenter.GetScore(ExpTerm.qid, doc.DocNo)
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
    
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.InName)
        
        out = open(self.OutName,'w')
        for lExpTerm in llExpTerm:
            query= lExpTerm[0].query
            print "working query [%s]" %(query)
            lDoc = ReadPackedIndriRes(self.CashDir + "/" + query,self.ReRankDepth)
            
            for ExpTerm in lExpTerm:
                ExpTerm.score = self.EvaluatePerTerm(ExpTerm, lDoc)
                print >>out, ExpTerm.dumps()
        out.close()
        
        
        
import sys

if 2 != len(sys.argv):
    print "conf"
    TermLabelViaDocRankingScoreC.ShowConf()
    sys.exit()
    
Evaluator = TermLabelViaDocRankingScoreC(sys.argv[1])
Evaluator.Process()
print "done"
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
