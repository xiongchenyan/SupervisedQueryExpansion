'''
Created on Mar 26, 2014
input:
    root dir: ->    partitioned data dir +    para dir
    base condor sub file
    K
    job name
do:
    form file names
    form para names (by traverse para dir)
    for each combination
        form conf file
        form sub file
    submit sub files
output:
    submit job ids and output location
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

class QExpSVMTrainFoldSubmiterC(object):
    def Init(self):
        self.RootDir = ""
        self.K = 5
        self.CondorSeedFile = ""
        self.NameCenter = FoldNameGeneratorC()
        self.CondorBase = cxCondorC()
        self.JobName = "QExpSVM"
        return
    
    
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.RootDir = conf.GetConf('rootdir')
        self.NameCenter.SetConf(ConfIn)
        self.K = int(conf.GetConf('k'))
        self.CondorSeedFile = conf.GetConf('condorseed')
        self.CondorBase.LoadSub(self.CondorSeedFile)
        self.JobName = conf.GetConf('jobname')
        
        return True
    
    @staticmethod
    def ShowConf():
        print "rootdir\nk\njobname\ncondorseed"
        FoldNameGeneratorC.ShowConf()
    
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
            
    
    def FormParaName(self):
        lFName = WalkDir(self.NameCenter.ParaDir()) #para index is exactly the para fname
        return lFName
    
    
    def FormFileName(self):
        lTrainName = []
        lDevName = []
        lFName = self.NameCenter.DataFileName() #id is same as location in lFName
        for FName in lFName:
            lTrainName.append(FName[0])
            lDevName.append(FName[2])
        return lTrainName,lDevName
    
    def FormConfForCombination(self,TrainName,DevName,ParaName):
        conf = cxConf()
        conf.SetConf('train',TrainName)
        conf.SetConf('dev',DevName)
        conf.SetConf('para',ParaName)
        
        FoldId = FoldNameGeneratorC.SplitFoldId(TrainName)
        ParaId = ntpath.basename(ParaName)
        OutName = self.NameCenter.EvaDir() + "/%s_%s_eval" %(FoldId,ParaId)        
        conf.SetConf('out',OutName)
        return conf
    
    
    def FormSubForConf(self,conf,ConfIndex):
        #form conf file name and write conf file (solely index)
        #change the last arguments to conf file
        #change log output error fields
        
        condor = deepcopy(self.CondorBase)
        
        ConfFName = self.NameCenter.ConfDir() + "_%d" %(ConfIndex)
        conf.dump(ConfFName)
        oldargu = list(condor.GetCondor('arguments'))
        oldargu[len(oldargu) - 1] = ConfFName
        
        condor.SetCondor('arguments',oldargu)
        condor.SetCondor('output',condor.GetCondor('output') + self.JobName + "_%d"%(ConfIndex))
        condor.SetCondor('error',condor.GetCondor('error') + self.JobName + "_%d"%(ConfIndex))
        condor.SetCondor('log',condor.GetCondor('log') + self.JobName + "_%d"%(ConfIndex))
        return condor
    
    
    
    
    def Process(self):
        
        print "start submit train folds"
        
        lParaName = self.FormParaName()
        print "para name: %s" %(json.dumps(lParaName))
        lTrainName,lDevName = self.FormFileName()
        print "train name: %s\ndev name:%s" %(json.dumps(lTrainName),json.dumps(lDevName))
        
        
        
        
        JobId = 0
        lSub = []        
        for i in range(len(lParaName)):
            for j in range(len(lTrainName)):
                print "combination [%d][%d]" %(i,j)
                conf = self.FormConfForCombination(lTrainName[j], lDevName[j], lParaName[i])
                print "conf:\n %s" %(json.dumps(conf.hConf))                
                Sub = self.FormSubForConf(conf, JobId)
                print "sub:\n %s" %(json.dumps(Sub.hConf))                
                lSub.append(Sub)
                
        CondorSubmiter = CondorSubmiterC()
        CondorSubmiter.WorkDir = self.NameCenter.SubDir()
        lJobId = CondorSubmiter.Submit(lSub, self.JobName)        
        print "submitted job ids:\n%s" %(json.dumps(lJobId,indent=1))        
        return lJobId
    
    
        
        
        
        
        
        
        
        
        
        
        
        
    