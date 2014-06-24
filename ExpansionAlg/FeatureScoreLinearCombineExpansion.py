'''
Created on Jun 24, 2014
do expansion by calculate term score via linear combination of feature scores
in:
    exp term, with feature score
        input feature score should be min-max normalized? (and only the to explore feature is kept)
    query, doc cache, etc.
    feature score combine weight
    exp term #
do:
    combine feature score as term ranking score, sort and use top expterm number
    output expterms, the ExpansionSingleRunCenter will use them to expansion and evaluation
@author: chenyan
'''


import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from base.ExpTerm import *
from operator import attrgetter
from CrossValidation.ParameterSet import *



class FeatureScoreLinearCombineExpansionC(cxBaseC):
    
    def Init(self):
        self.NumOfTerm = 10
        self.ExpTermIn = ""
        self.lFeatureWeight = []
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.NumOfTerm = int(conf.GetConf('numofexpterm',self.NumOfTerm))
        self.ExpTermIn = conf.GetConf('in')
        FeatureWeightStr = conf.GetConf('featureweight')
        self.lFeatureWeight = self.SegFeatureWeightStr(FeatureWeightStr)
        return True
    
    @staticmethod
    def ShowConf():
        print "in\nfeatureweight\nnumofexpterm"
        
        
        
        
    def SegFeatureWeightStr(self,FeatureWeightStr):
        if FeatureWeightStr == '':
            return []
        lWeight = [float(item) for item in FeatureWeightStr.split('_')]
        lFeatureWeight = [max(0,1 - sum(lWeight))] + lWeight
        return lFeatureWeight
    
    
    def CalcExpTermScore(self,ExpTerm):
        #the feature order defined via string order
        lFeature = ExpTerm.hFeature.items()
        lFeature.sort(key = lambda item: item[0])
        score = 0
        for i in range(len(lFeature)):
            weight = 0
            if i < len(self.lFeatureWeight):
                weight = self.lFeatureWeight[i]
            score += weight * lFeature[i][1]
        ExpTerm.score = score
        return ExpTerm
    
    def Process(self,qid='',query='',lDoc=[]):
        #qid, query, lDoc are used to keep consistency with 
        lExpTerm = []
        llInExpTerm = ReadQExpTerms(self.ExpTermIn)
        for lInExpTerm in llInExpTerm:
            if qid != '':
                if lInExpTerm[0].qid != qid:
                    #only deal with current qid
                    continue
            lInExpTerm  = MinMaxFeatureNormalize(lInExpTerm)
            for ExpTerm in lInExpTerm:                
                ExpTerm = self.CalcExpTermScore(ExpTerm)
                lExpTerm.append(ExpTerm)
        lExpTerm.sort(key = lambda item: item.score,reverse = True)
        lExpTerm = NormalizeExpTermWeight(lExpTerm)
        return lExpTerm[:self.NumOfTerm]
        
    def SetParameter(self,ParaSet):
        if 'featureweight' in ParaSet.hPara:
            self.lFeatureWeight = self.SegFeatureWeightStr(ParaSet.hPara['featureweight'])
        if 'numofexpterm' in ParaSet.hPara:
            self.NumOfExpTerm = int(ParaSet.hPara['numofexpterm'])
        return True    
        