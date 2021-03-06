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
from cxBase.base import cxConf
import json
from base.ExpTerm import ExpTermC
from cxBase.WalkDirectory import WalkDir
from CrossValidation.FoldNameGenerator import FoldNameGeneratorC
from CrossValidation.CVParaResCollector import CVParaResCollectorC
import ntpath
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



class QExpParaEvaResCollectorC(CVParaResCollectorC):
    #get the best performance for each fold
    def Init(self):
        super(QExpParaEvaResCollectorC,self).Init()
#         self.WorkDir = ""
#         self.hFoldBest = {} #Fold Index -> [para p, best acc]
        self.MainEvaMethod = 'fmeasure'
        
    def SetConf(self,ConfIn):
        super(QExpParaEvaResCollectorC,self).SetConf(ConfIn)
        conf = cxConf(ConfIn)
        self.MainEvaMethod = conf.GetConf('mainevamethod')
        return True
    def FilterEvaResFName(self,FName):
        vCol = ntpath.basename(FName).split('_')
        if len(vCol) != 3:
            return False
        if vCol[2] != 'eval':
            return False
        return True
    
    @staticmethod
    def ShowConf():
        CVParaResCollectorC.ShowConf()
        print "mainevamethod"
    

    
    def SplitFoldParaId(self,EvaName):
        vCol = ntpath.basename(EvaName).split('_')
        FoldIndex = -1
        ParaIndex = -1
        if len(vCol) == 3:
            if vCol[2] == 'eval':
                FoldIndex = int(vCol[0])
                ParaIndex = int(vCol[1])
        return FoldIndex,ParaIndex
    
    def LoadEvaMetric(self,EvaName):
        In = open(EvaName)
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
            
        score = FMeasure
        if self.MainEvaMethod == 'precision':
            score =  Precision
        if self.MainEvaMethod == "recall":
            score = Recall
        print "load eva metric [%f] from [%s]" %(score,EvaName)
        return score
    
    
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
    

 