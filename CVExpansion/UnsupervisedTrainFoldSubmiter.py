'''
Created on Mar 31, 2014
submit train folder of unsupervised methods
submit for the ExpansionSingleRunPipeRun
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from CrossValidation.CVJobSubmiter import *
import ntpath


class UnsupervisedTrainFoldSubmiterC(CVJobSubmiterC):
    
    def InitCollectRes(self):
        #sub class will collect and set data sources here
        print "unsupervised train folds, nothing to collect"
        return True
    
    def GenerateConfForPair(self,FName,ParaName):
        #set conf here, modify parameter
        conf = deepcopy(self.ConfBase)
        
        #to set fields:
            #in = train
            #paraset = paraname
            #evaoutdir = eval/fold_para_eval/
        
        conf.SetConf('in',FName[0])
        conf.SetConf('paraset',ParaName)
        FoldIndex = self.Namer.SplitFoldId(FName[0])
        conf.SetConf('evaoutdir',self.Namer.EvaDir() + "/%d_%s_eval/" %(FoldIndex,ntpath.basename(ParaName)))        
        return conf
    
    
    
    
    
def UnsupervisedTrainFoldSubmiterUnitRun(ConfIn):
    Submiter = UnsupervisedTrainFoldSubmiterC(ConfIn)
    Submiter.Process()    
    return True