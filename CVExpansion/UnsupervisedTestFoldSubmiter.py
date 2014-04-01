'''
Created on Mar 31, 2014

@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from CrossValidation.CVJobSubmiter import *
from UnsupervisedEvaResCollector import *
from CrossValidation.FoldNameGenerator import *
import ntpath




class UnsupervisedTestFoldSubmiterC(CVJobSubmiterC):
    
    def InitCollectRes(self):
        #sub class will collect and set data sources here
        print "collecting best para for each fold"
        ResCollector = UnsupervisedEvaResCollectorC(self.ConfIn)
        self.hFoldPara = ResCollector.Process()
        return True

    #tbd    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        conf = deepcopy(self.ConfBase)
        
        #to set fields:
            #in = test
            #paraset = paraname
            #evaoutdir = Namer.PreDir() + fold_para_pre/
        
        conf.SetConf('in',FName[1])
        conf.SetConf('paraset',ParaName)
        FoldIndex = self.Namer.SplitFoldId(FName[0])
        conf.SetConf('evaoutdir',self.Namer.PredictDir() + "/%d_%s/" %(FoldIndex,ntpath.basename(ParaName)))        
        return conf
    
    def FNameParaPairValid(self,FName,ParaName):
        #check whether this paraset appliable to this FName
        #if not return False
        #using information in self.hxxx
        
        #get the fold id and para id from FName and ParaName
        FoldId = int(FoldNameGeneratorC.SplitFoldId(FName))
        ParaId = int(ntpath.basename(ParaName))
        if not FoldId in self.hFoldPara:
            print "fold [%d]'s best para not load" %(FoldId)
            return False
        if ParaId == self.hFoldPara[FoldId][0]:
            return True      
        return False
    
    @staticmethod
    def ShowConf():
        UnsupervisedEvaResCollectorC.ShowConf()
        CVJobSubmiterC().ShowConf()
        return True
        
        
        
    
    
def UnsupervisedTestFoldSubmiterUnitRun(ConfIn):
    Submiter = UnsupervisedTestFoldSubmiterC(ConfIn)
    Submiter.Process()        
    return True
    