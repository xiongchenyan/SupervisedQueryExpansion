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

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.base import *
import json
from base.ExpTerm import *
from cxBase.WalkDirectory import *
from CrossValidation.FoldNameGenerator import *
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath

from QExpParaEvaResCollect import *




class QExpSVMTestFoldSubmiterC(object):
    
    def Init(self):
        self.WorkDir = ""
        self.NameCenter = FoldNameGeneratorC()
        self.K = 5
        self.EvaResCollector = QExpParaEvaResCollectorC()
        self.hFoldBestP = {}
        self.CondorBase = cxCondorC()
        self.JobName = 'test'
        return
    
    def SetConf(self,ConfIn):
        self.NameCenter.SetConf(ConfIn)
        self.EvaResCollector.SetConf(ConfIn)
        self.WorkDir = self.NameCenter.RootDir
        self.K = self.NameCenter.K
        conf = cxConf(ConfIn)
        self.CondorBase.LoadConf(conf.GetConf('condorseed'))
        self.JobName = conf.GetConf('jobname')
        
        return True
    
    @staticmethod
    def ShowConf():
        FoldNameGeneratorC.ShowConf()
        QExpParaEvaResCollectorC.ShowConf()
        print "condorseed\njobname"
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
            
    
    
    
    def LookUpFoldParaFName(self,TestName):
        FoldIndex = int(FoldNameGeneratorC.SplitFoldId(TestName))
        if not FoldIndex in self.hFoldBestP:
            print "fold [%d] best parameter not loaded" %(FoldIndex)
            return False
        ParaP = self.hFoldBestP[FoldIndex][0]
        ParaFName = self.NameCenter.ParaDir() + "/%d"%(ParaP)
        return ParaFName
    
    def LoadFName(self):
        lFName = self.NameCenter.DataFileName()
        lTrain = [TrainName for TrainName,TestName,DevName in lFName]
        lTest = [TestName for TrainName,TestName,DevName in lFName]
        return lTrain,lTest
    
    
    def MatchOutName(self,TestName):
        FoldId = FoldNameGeneratorC.SplitFoldId(TestName)
        OutName = self.NameCenter.PredictDir() + "%d" %(FoldId)
        return OutName
    
    
    
    def FormConfForFold(self,TrainName,TestName):
        ParaName = self.LookUpFoldParaFName(TestName)
        OutName = self.MatchOutName(TestName)
        conf = cxConf()
        conf.SetConf('train', TrainName)
        conf.SetConf('test',TestName)
        conf.SetConf('out',OutName)
        conf.SetConf('para',ParaName)
        return conf
    
    
    def FormSubForConf(self,conf,ConfIndex):
        condor = deepcopy(self.CondorBase)        
        ConfFName = self.NameCenter.ConfDir() + "_%d" %(ConfIndex)
        conf.dump(ConfFName)
        oldargu = list(condor.GetCondor('arguments'))
        oldargu[len(oldargu) - 1] = ConfFName
        
        condor.SetField('arguments',oldargu)
        condor.SetField('output',condor.GetCondor('output') + self.JobName + "_%d"%(ConfIndex))
        condor.SetField('error',condor.GetCondor('error') + self.JobName + "_%d"%(ConfIndex))
        condor.SetField('log',condor.GetCondor('log') + self.JobName + "_%d"%(ConfIndex))
        return condor
    
    
    
    def Process(self):
        
        #collect result
        self.hFoldBestP = self.EvaResCollector.Process()
        print "best per fold res:\n%s" %(json.dumps(self.hFoldBestP,indent=1))
        lTrain,lTest = self.LoadFName()
        lSub = []        
        for i in range(len(lTrain)):
            conf = self.FormConfForFold(lTrain[i], lTest[i])
            condor = self.FormSubForConf(conf, i)
            lSub.append(condor)            
        Submitter = CondorSubmiterC()
        Submitter.WorkDir = self.NameCenter.SubDir()
        return Submitter.Submit(lSub, self.JobName)
        
    
    
        
        
        