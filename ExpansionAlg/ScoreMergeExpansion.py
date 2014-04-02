'''
Created on Apr 1, 2014
perfom like IndriExpansion:
input: scored term + base term + para
output: merged term
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from base.ExpTerm import *
from operator import attrgetter
from CrossValidation.ParameterSet import *


class ScoreMergeExpansionC(cxBaseC):
    
    def Init(self):
        self.lBaseTerm = []
        self.hBaseTerm = {}
        self.Alpha = 0.5
        self.NumOfTerm = 10
        self.ExpTermIn = ""
        self.DefaultMinScore = 0.001
        return
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.Alpha = float(conf.GetConf('alpha'))
        self.lBaseTerm = self.LoadBaseTerm(conf.GetConf('baseterm'))
        self.NumOfTerm = int(conf.GetConf('numofexpterm'))
        self.ExpTermIn = conf.GetConf('in')
        return True
    
    @staticmethod
    def ShowConf():
        print "alpha\nbaseterm\nnumofexpterm\nin"
    
    def LoadBaseTerm(self,Path):
        llExpTerm = ReadQExpTerms(Path)
        for lExpTerm in llExpTerm:
            self.lBaseTerm.extend(lExpTerm)
            
        for i in range(len(self.lBaseTerm)):
            self.hBaseTerm[self.lBaseTerm[i].Key()] = i
        return True
    
    
    def MergeScore(self,ExpTerm):
        
        key = ExpTerm.Key()    
        BaseScore = self.DefaultMinScore
        if key in self.hBaseExpTerm:
                BaseScore = self.lBaseExpTerm[self.hBaseExpTerm[key]].score
        ThisScore = BaseScore * (1 + self.Alpha * ExpTerm.score)    
        ExpTerm.score = ThisScore
        return ExpTerm
    
    
    
    def Process(self):
        lExpTerm = []
        llInExpTerm = ReadQExpTerms(self.ExpTermIn)
        for lInExpTerm in llInExpTerm:
            for ExpTerm in lInExpTerm:
                if ExpTerm.score < 0.5:
                    #discard those with p<0.5
                    continue
                ExpTerm = self.MergeScore(ExpTerm)
                lExpTerm.append(ExpTerm)
        lExpTerm = NormalizeExpTermWeight(lExpTerm)
        return lExpTerm[:self.NumOfTerm]
    
    
    def SetParameter(self,ParaSet):
        if 'alpha' in ParaSet.hPara:
            self.Alpha = ParaSet.hPara['alpha']
        if 'numofexpterm' in ParaSet.hPara:
            self.NumOfExpTerm = int(ParaSet.hPara['numofexpterm'])
        return True



def ScoreMergeExpansionUnitRun(ConfIn):
    conf = cxConf(ConfIn)
    OutName = conf.GetConf('out')
    Expansioner = ScoreMergeExpansionC(ConfIn)
    lExpTerm = Expansioner.Process()
    out = open(OutName,'w')
    for ExpTerm in lExpTerm:
        print >> out,ExpTerm.dump()
    out.close()
    return True


    
    

                