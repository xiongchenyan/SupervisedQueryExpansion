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
        self.MainEvaMethod = 'precision'
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        NameCenter = FoldNameGeneratorC()
        NameCenter.RootDir = conf.GetConf('workdir')
        self.WorkDir =  NameCenter.EvaDir()
        self.MainEvaMethod = conf.GetConf('mainevamethod')
        return True
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)           
    
    @staticmethod
    def ShowConf():
        print "workdir\nmainevamethod"
    
    def ProcessOneFile(self,FName):
        vCol = FName.split('/')
        FoldIndex,ParaIndex = SegFoldParaIndexFromFName(vCol[len(vCol) - 1])
        print "working fold [%d] para [%d] file [%s]" %(FoldIndex,ParaIndex,FName)
        if -1 == FoldIndex:
            return True
        Mea = self.ReadMeasure(FName)
        print "Eva Mea [%f]" %(Mea)
        if not FoldIndex in self.hFoldBest:
            self.hFoldBest[FoldIndex] = [0,0]
        if Mea > self.hFoldBest[FoldIndex][1]:
            print "better than old [%d][%f]"%(self.hFoldBest[FoldIndex][0],
                                              self.hFoldBest[FoldIndex][1])
            self.hFoldBest[FoldIndex] = [ParaIndex,Mea]
        return True
    
    def Process(self):
        lFName = WalkDir(self.WorkDir)
        for FName in lFName:
            self.ProcessOneFile(FName)
        return dict(self.hFoldBest)
    
    
    
    def ReadMeasure(self,FName):
        #tbd:notsure
        In = open(FName)
        lContTable = json.load(In)
        Precision = 0
        Recall = 0
        if (lContTable[1][0] + lContTable[1][1]) != 0:
            Precision = float(lContTable[1][1]) / float((lContTable[1][0] + lContTable[1][1]))
            
        if (lContTable[0][1] + lContTable[1][1]) != 0:
            Recall = float(lContTable[1][1]) / float(lContTable[0][1] + lContTable[1][1])
        if (Precision + Recall) == 0:
            FMeasure = 0
        else:
            FMeasure = 2 * Precision * Recall / (Precision + Recall)
        if self.MainEvaMethod == 'precision':
            return Precision
        if self.MainEvaMethod == "recall":
            return Recall
        return FMeasure
    
    


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
    

 