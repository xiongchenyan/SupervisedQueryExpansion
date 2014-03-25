'''
Created on Mar 25, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')

from CrossValidation.ParameterSet import *
from base.ExpTerm import *
from CrossValidation.RandomSplit import *
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
    
    



def ExpTermDataSpliterUnitRun(ConfIn):
    ExpTermDataSpliter = ExpTermDataSpliterC(ConfIn)
    ExpTermDataSpliter.Process()
    return True


def ExpTermDataAndParaSplitRun(ConfIn):
    ExpTermDataSpliterUnitRun(ConfIn)
    conf = cxConf(ConfIn)
    
    ParaSetIn = conf.GetConf('para')
    OutDir = conf.GetConf('rootdir') + '/para/'
    
    SplitParaSetToFolder(ParaSetIn,OutDir)
    return True
    
     
     