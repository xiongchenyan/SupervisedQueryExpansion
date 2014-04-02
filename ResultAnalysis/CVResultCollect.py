'''
Created on Apr 1, 2014
collect evaluation result perfold
run on boston
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from CrossValidation.FoldNameGenerator import *
from AdhocEva.AdhocMeasure import *
from cxBase.WalkDirectory import *
from operator import itemgetter
import sys

'''
traverse all file in predict dir
keep those with per q eva
merge and calculate evaluation res
output

'''


def FetchPerQEvaName(Namer):
    lFName = WalkDir(Namer.PredictDir())
    lRes = []
    for FName in lFName:
        if 'PerQEva' in FName:
            lRes.append(FName)
    return lRes



def ResultCollect(ConfIn):
    Namer = FoldNameGeneratorC(ConfIn)
    conf = cxConf(ConfIn)
    OutName = conf.GetConf('out')
    
    
    lPerQEvaName = FetchPerQEvaName(Namer)
    
    
    lPerQEva = []
    for FName in lPerQEvaName:
        lPerQEva.extend(ReadPerQEva(FName))
        
    lPerQEva.sort(key=itemgetter(0))
    MeanMeasure = AdhocMeasureC()
    out = open(OutName,'w')
    for Eva in lPerQEva:
        print >> out,Eva[0] + "\t" + Eva[1].dumps()
        MeanMeasure += Eva[1]
    MeanMeasure /= float(len(lPerQEva))
    print >>out, 'mean\t%s' %(MeanMeasure.dumps())
    out.close()
    return True



if 2 != len(sys.argv):
    print "1 para conf\nout"
    FoldNameGeneratorC.ShowConf()
    sys.exit()
    
    
ResultCollect(sys.argv[1])
print "finished"
    
    
