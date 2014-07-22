'''
Created on Mar 25, 2014

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
    
    def LoadData(self):
        llExpTerm = ReadQExpTerms(self.InName)
        print "load to split query [%d]" %(len(llExpTerm))
        return llExpTerm
    
    def OutData(self,llExpTerm,OutName):
        out = open(OutName,'w')
        for lExpTerm in llExpTerm:
            for ExpTerm in lExpTerm:
                print >>out, ExpTerm.dump()
        out.close()
        return True
    
    
class ExpQueryDataSpliterC(DataSpliterC):
    
    def LoadData(self):
        lData = []
        for line in open(self.InName):
            lData.append(line.strip())
        return lData
    def OutData(self,lData,OutName):
        out = open(OutName,'w')
        for line in lData:
            print >>out, line
        out.close()
        return True


def ExpTermDataSpliterUnitRun(ConfIn):
    ExpTermDataSpliterC.ShowConf()
    ExpTermDataSpliter = ExpTermDataSpliterC(ConfIn)
    ExpTermDataSpliter.Process()
    return True


def ExpQueryDataSpliterUnitRun(ConfIn):
    ExpQueryDataSpliterC.ShowConf()
    DataSpliter = ExpQueryDataSpliterC(ConfIn)
    DataSpliter.Process()
    return True

def ExpTermDataAndParaSplitRun(ConfIn):
    conf = cxConf(ConfIn)
    print "para\nrootdir"
    InputType = conf.GetConf('inputtype','qterm')
    if InputType == 'qterm':
        ExpTermDataSpliterUnitRun(ConfIn)
    if InputType == 'query':
        ExpQueryDataSpliterUnitRun(ConfIn)
    
    
    Namer = FoldNameGeneratorC()
    Namer.RootDir = conf.GetConf('rootdir')    
    ParaSetIn = conf.GetConf('para')
    SplitParaSetToFolder(ParaSetIn,Namer.ParaDir())
    return True
    
     
     