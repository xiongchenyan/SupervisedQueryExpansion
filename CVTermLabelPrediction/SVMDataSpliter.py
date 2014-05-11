'''
Created on Mar 25, 2014

May 9, 2014 modify:
add function to filter out feature that hit 0 positive training insitence in training data

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from CrossValidation.ParameterSet import *
from base.ExpTerm import *
from CrossValidation.RandomSplit import *
from CrossValidation.FoldNameGenerator import *
class ExpTermDataSpliterC(DataSpliterC):
    
    def Init(self):
        super(ExpTermDataSpliterC,self).Init()
        self.FilterNoPosFeatureInTrain = False
        
    def SetConf(self,ConfIn):
        super(ExpTermDataSpliterC,self).SetConf(ConfIn)
        conf =cxConf(ConfIn)
        self.FilterNoPosFeatureInTrain = bool(int(conf.GetConf('filternonpos',0)))
        return True
    
    @staticmethod
    def ShowConf():
        DataSpliterC.ShowConf()
        print "filternonpos"
    
    
    
    
    def LoadData(self):
        llExpTerm = ReadQExpTerms(self.InName)
        print "load to split query [%d]" %(len(llExpTerm))
        return llExpTerm
    
    def OutData(self,llExpTerm,OutName):
        out = open(OutName,'w')
        
        if self.FilterNoPosFeatureInTrain & ('train' in OutName):
            lAllTerm = []
            for lExpTerm in llExpTerm:
                lAllTerm.extend(lExpTerm)
            lFilterTerm = ExpTermC.FilterNonPosFeature(lAllTerm)
            llExpTerm = ExpTermC.SplitByQid(lFilterTerm)        
        
        for lExpTerm in llExpTerm:
            for ExpTerm in lExpTerm:
                print >>out, ExpTerm.dump()
        out.close()
        return True
    
    



def ExpTermDataSpliterUnitRun(ConfIn):
    ExpTermDataSpliterC.ShowConf()
    ExpTermDataSpliter = ExpTermDataSpliterC(ConfIn)
    ExpTermDataSpliter.Process()
    return True


def ExpTermDataAndParaSplitRun(ConfIn):
    conf = cxConf(ConfIn)
    print "para\nrootdir"
    ExpTermDataSpliterUnitRun(ConfIn)
    
    Namer = FoldNameGeneratorC()
    Namer.RootDir = conf.GetConf('rootdir')    
    ParaSetIn = conf.GetConf('para')
    SplitParaSetToFolder(ParaSetIn,Namer.ParaDir())
    return True
    
     
     