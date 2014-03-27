'''
Created on Mar 25, 2014
input: the folder of submitted QExpSVMParaEvaRes
output: the best para index for each folder
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/LibSVM/libsvm/python/')
from cxBase.base import *
import json
from base.ExpTerm import *
from cxBase.WalkDirectory import *
from CrossValidation.FoldNameGenerator import *


def GenerateFoldParaEvaFName(FoldIndex,ParaIndex):
    return "%d_%d_eval" %(FoldIndex,ParaIndex)

def SegFoldParaIndexFromFName(FName):
    vCol = FName.split('_')
    FoldIndex = -1
    ParaIndex = -1
    if len(vCol) == 3:
        if vCol[2] == 'eval':
            FoldIndex = int(vCol[0])
            ParaIndex = int(vCol[1])
    return FoldIndex,ParaIndex



class QExpParaEvaResCollectorC(object):
    #get the best performance for each fold
    def Init(self):
        self.WorkDir = ""
        self.hFoldBest = {} #Fold Index -> [para p, best acc]
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        NameCenter = FoldNameGeneratorC()
        NameCenter.RootDir = conf.GetConf('workdir')
        self.WorkDir =  NameCenter.EvaDir()
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)           
    
    @staticmethod
    def ShowConf():
        print "workdir"
    
    def ProcessOneFile(self,FName):
        vCol = FName.split('/')
        FoldIndex,ParaIndex = SegFoldParaIndexFromFName(vCol[len(vCol) - 1])
        if -1 == FoldIndex:
            return True
        Acc = self.ReadACC(FName)
        if not FoldIndex in self.hFoldBest:
            self.hFoldBest[FoldIndex] = [0,0]
        if Acc > self.hFoldBest[FoldIndex]:
            self.hFoldBest[FoldIndex] = [ParaIndex,Acc]
        return True
    
    def Process(self):
        lFName = WalkDir(self.WorkDir)
        for FName in lFName:
            self.ProcessOneFile(FName)
        return dict(self.hFoldBest)
    
    
    
    def ReadACC(self,FName):
        #tbd:notsure
        In = open(FName)
        p_acc = json.load(In)
        return p_acc[0]
    
    


def QExpParaEvaResCollectorUnitTest(ConfIn):
    QExpParaEvaResCollectorC.ShowConf()
    print "out"
    conf = cxConf(ConfIn)
    OutName = conf.GetConf('out')
    Collector = QExpParaEvaResCollectorC(ConfIn)
    
    hDict = Collector.Process()
    out = open(OutName,'w')
    json.dump(hDict,out)
    out.close()
    
    print "done"
    return True
    

 