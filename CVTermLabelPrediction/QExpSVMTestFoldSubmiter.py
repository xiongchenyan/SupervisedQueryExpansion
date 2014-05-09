'''
Created on Mar 26, 2014
input: work dir, k
do:
    collect cv train-dev para evaluation results (Call QExpParaEvaResCollect)
    for each fold:
        find best para fname
        find train-test data fname
        form conf
        form sub
    submit
return jobid
@author: cx
'''




'''
TBD:
inherite from CVJobSubmiter, and discard duplicated implementation
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
import json
from base.ExpTerm import *
from cxBase.WalkDirectory import *
from CrossValidation.FoldNameGenerator import *
from CrossValidation.CVJobSubmiter import CVJobSubmiterC
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath

from QExpParaEvaResCollect import *


class QExpSVMTestFoldSubmiterC(CVJobSubmiterC):
    
    def InitCollectRes(self):
        #sub class will collect and set data sources here
        print "collecting best para for each fold"
        ResCollector = QExpParaEvaResCollectorC(self.ConfIn)
        self.hFoldPara = ResCollector.Process()
        return True
    
    def MatchOutName(self,TestName):
        FoldId = FoldNameGeneratorC.SplitFoldId(TestName)
        OutName = self.Namer.PredictDir() + "%d" %(FoldId)
        return OutName
    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        OutName = self.MatchOutName(FName[1])
        conf = cxConf()
        conf.SetConf('train', FName[0])
        conf.SetConf('test',FName[1])
        conf.SetConf('out',OutName)
        conf.SetConf('para',ParaName)
        return conf
    
    def FNameParaPairValid(self,FName,ParaName):
        #check whether this paraset appliable to this FName
        #if not return False
        #using information in self.hxxx
        
        #get the fold id and para id from FName and ParaName
        FoldId = int(FoldNameGeneratorC.SplitFoldId(FName[1]))
        ParaId = int(ntpath.basename(ParaName))
        if not FoldId in self.hFoldPara:
            print "fold [%d]'s best para not load" %(FoldId)
            return False
        if ParaId == self.hFoldPara[FoldId][0]:
            return True      
        return False
    
    @staticmethod
    def ShowConf():
        QExpParaEvaResCollectorC.ShowConf()
        CVJobSubmiterC().ShowConf()
        return True    
        
        
        