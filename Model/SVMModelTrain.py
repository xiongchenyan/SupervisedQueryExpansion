'''
Created on Mar 20, 2014
input: read training data: llExpTerm[query][term] + lParaSet + K
    if len(lParaSet) = 1 then, use it train model
    else: K fold cv on llExpTerm(query dimension) choose the best parameter, and train
return a SVM model
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')

from LibSVMRelate.SVMBase import *
from svmutil import *
from CrossValidation.ParameterSet import *
from CrossValidation.RandomSplit import *
from cxBase.base import *
from base.ExpTerm import *

class SVMModelTrainC(object):
    def Init(self):
        return
    
    
    def __init__(self):
        self.Init()
        
        
    @staticmethod
    def ShowConf():
        return
    

    
    
    def OneFoldTrainTest(self,lTrainLabel,lTrainData,lTestLabel,lTestData,lSVMPara):
        #for each para, train and test, record performance in lPerformance (1-1 with lSVMPara)
        lPerformance = []
        
        SVMProb =  svm_problem(lTrainLabel,lTrainData)
        for SVMPara in lSVMPara:
            ParaStr = SVMPara.dump()
            print "start train with para [%s]" %(ParaStr)
            param = svm_parameter(ParaStr)
            SVMModel = svm_train(SVMProb,param)
            
            p_label,p_acc,p_val = svm_predict(lTestLabel,lTestData,SVMModel)
            lPerformance.append(p_acc[0]) #we are classification
        return lPerformance
    
    def SingleTrain(self,llExpTerm,SVMPara):
        lScore,lhFeature = SplitLabelAndFeature(llExpTerm)
        SVMModel = svm_train(lScore,lhFeature,SVMPara.dump())
        return SVMModel
    
    
    def Train(self,llExpTerm,lSVMPara,K=0):
        if len(lSVMPara) == 1:
            return self.SingleTrain(llExpTerm, lSVMPara[0])
            
        
        #now we need CV
        llSplit = RandomSplit(llExpTerm,K)
        lPerformance = []
        cnt = 0
        for llTrainExpTerm,llTestExpTerm in llSplit:
            print "start fold [%d]" %(cnt)
            cnt += 1
            lTrainLabel,lTrainData = SplitLabelAndFeature(llTrainExpTerm)
            lTestLabel,lTestData = SplitLabelAndFeature(llTestExpTerm)
            lCurrentFoldPerformance = self.OneFoldTrainTest(lTrainLabel, lTrainData, lTestLabel, lTestData, lSVMPara)
            if [] == lPerformance:
                lPerformance = lCurrentFoldPerformance
            else:
                for i in range(len(lPerformance)):
                    lPerformance[i] += lCurrentFoldPerformance[i]
        for i in range(len(lPerformance)):
            lPerformance[i] /= float(K)
        p = lPerformance.index(max(lPerformance))
        print "best para [%s] accuracy [%f]" %(lSVMPara[p].dump(),lPerformance[p])
        
        
        print "start apply on train"
        return self.SingleTrain(llExpTerm, lSVMPara[p])
        
        
        
            
                
            
        
def SVMModelTrainUnitTest(ConfIn):
    print "in\nparaset\nk\nout"
    SVMModelTrainC.ShowConf()
    conf = cxConf(ConfIn)
    ExpTermInName = conf.GetConf('in')
    ParaSetInName = conf.GetConf('paraset')
    K = int(conf.GetConf('k'))
    OutName = conf.GetConf('out')
    SVMTrain = SVMModelTrainC()
    
    llExpTerm = ReadQExpTerms(ExpTermInName)
    lSVMPara = ReadSVMParaSet(ParaSetInName)
    
    SVMModel = SVMTrain.Train(llExpTerm, lSVMPara, K)
    
    svm_save_model(OutName,SVMModel)
        
    return True
            
        
        
        
            
            
        
                
        
     
