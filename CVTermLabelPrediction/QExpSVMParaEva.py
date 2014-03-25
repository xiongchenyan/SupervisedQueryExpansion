'''
Created on Mar 25, 2014
input: train name + dev name + paraname
output: accuracy on dev
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')
site.addsitedir('/bos/usr0/cx/LibSVM/libsvm/python/')
from LibSVMRelate.SVMBase import *
from svmutil import *
from cxBase.base import *
import json
from base.ExpTerm import *

from LibSVMRelate.SVMRunSinglePara import *


class QExpSVMParaEvaC(SVMRunSingleParaC):
    
    def LoadData(self,InName):
        llExpTerm = ReadQExpTerms(InName)
        lY,lX = SplitLabelAndFeature(llExpTerm,True)              
        return [lY,lX]
    
    def DumpPrediction(self,OutName,TestInName ,p_label,p_val):
        return True
    
    
    


def QExpSVMParaEvaUnitRun(ConfIn):    
    conf = cxConf(ConfIn)    
    TrainInName = conf.GetConf('train') 
    TestInName = conf.GetConf('dev')
    ParaInName = conf.GetConf('para')
    OutName = conf.GetConf('out')
    QExpSVMParaEva = QExpSVMParaEvaC()    
    QExpSVMParaEva.Process(TrainInName, TestInName, ParaInName,OutName)
    return True