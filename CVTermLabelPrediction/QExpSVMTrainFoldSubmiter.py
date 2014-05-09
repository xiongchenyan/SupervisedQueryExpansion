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
from CrossValidation.CVJobSubmiter import CVJobSubmiterC
from condor.CondorBase import *
from condor.CondorSubmiter import *
import ntpath

        
        
class QExpSVMTrainFoldSubmiterC(CVJobSubmiterC):        
    def GenerateConfForPair(self,FName,ParaName):
        conf = cxConf()
        conf.SetConf('train',FName[0])
        conf.SetConf('dev',FName[2])
        conf.SetConf('para',ParaName)
        
        FoldId = FoldNameGeneratorC.SplitFoldId(FName[0])
        ParaId = ntpath.basename(ParaName)
        OutName = self.Namer.EvaDir() + "/%s_%s_eval" %(FoldId,ParaId)        
        conf.SetConf('out',OutName)
        return conf
        
        
        
        
        
        
        
        
    