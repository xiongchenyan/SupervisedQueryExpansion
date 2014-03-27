'''
Created on Mar 26, 2014
input: a hFold[FoldIndex]->BestParaIndex (the output of QExpParaEvaResCollect)
        work dir
       fold id 
do:
    read parameter
    read fold data->train + dev -> test
    train model on train + dev with para
    apply on test, get prediction
output predicted data to data folder
output accuracy on eva folder    
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')
site.addsitedir('/bos/usr0/cx/LibSVM/libsvm/python/')
from cxBase.base import *
import json
from base.ExpTerm import *
from svmutil import *
from LibSVMRelate.SVMRunSinglePara  import *
from QExpSVMParaEva import *

class QExpSVMPerFoldPredictorC(QExpSVMParaEvaC):
    

    def DumpPrediction(self,OutName,TestInName ,p_label,p_val):
        #everything is the same, 
        #just need to load TestInName and merge it with p_val's second score(which is p(1))
        
        llExpTerm = ReadQExpTerms(TestInName)
        
        out = open(OutName,'w')
        index = 0
        for lExpTerm in llExpTerm:
            for ExpTerm in lExpTerm:
                ExpTerm.score = p_val[index][0] #tbd: check p_val output format
                print >>out,ExpTerm.dump()
        out.close()
        
        
        
        
        
        
        
def QExpSVMPerFOldPredictorRun(ConfIn):
    print "train\ntest\npara\nout"
    conf = cxConf(ConfIn)
    TrainInName = conf.GetConf('train')
    TestInName = conf.GetConf('test')
    ParaInName = conf.GetConf('para')
    OutName = conf.GetConf('out')    
    
    Predictor = QExpSVMPerFoldPredictorC()
    Predictor.Process(TrainInName, TestInName, ParaInName, OutName)

    return True