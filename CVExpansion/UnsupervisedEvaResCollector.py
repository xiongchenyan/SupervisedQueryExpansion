'''
Created on Mar 31, 2014
collect res
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from CrossValidation.CVParaResCollector import *
from AdhocEva.AdhocMeasure import *

class UnsupervisedEvaResCollectorC(CVParaResCollectorC):
    
    def SplitFoldParaId(self,EvaName):
        vCol = EvaName.split('/')
        Target = vCol[len(vCol) - 2]
        lMid = Target.split('_')
        FoldId = int(lMid[0])
        ParaId = int(lMid[1])               
        return FoldId,ParaId
    
    
    def LoadEvaMetric(self,EvaName):
        EvaMetric = 0
        for line in open(EvaName):  
            line = line.strip()          
            Measure = AdhocMeasureC(line)
            EvaMetric = Measure.err
        return EvaMetric    

    def FilterEvaResFName(self,EvaName):
        if 'MeanVsPara' in EvaName:       
            return True
        return False
    
    
    
    
def UnsupervisedEvaResCollectorUnitRun(ConfIn):
    Collector = UnsupervisedEvaResCollectorC(ConfIn)
    Collector.Process()    
    return True
