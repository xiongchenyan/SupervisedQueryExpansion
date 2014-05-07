'''
Created on May 7, 2014
input: workdir, k
do: go through all target file in pred dir, calculate the precision, recall, accuracy and cat all terms to one file 
output: to out dir
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')

from CrossValidation.FoldNameGenerator import *
from AdhocEva.AdhocMeasure import *
from cxBase.WalkDirectory import *
import sys
import json


if 2 != len(sys.argv):
    print "1 para: workdir"
    sys.exit()
    
    
Namer = FoldNameGeneratorC()
Namer.RootDir = sys.argv[1]
Namer.K = 5


OutExpTerm = open(Namer.OutDir() + "/QExpTermPredict",'w')
OutEva = open(Namer.OutDir() + "/predicteve",'w')
lConfMtx = [[0,0],[0,0]]
for i in range(Namer.K):
    InName = Namer.PredictDir() + "/%d_pre" %(i)
    for line in open(InName):
        print >>OutExpTerm,line
    AccIn = open(InName.replace('_pre",'),'r')
    lMidConfMtx = json.load(AccIn)
    for i in range(len(lConfMtx)):
        for j in range(len(lConfMtx[i])):
            lConfMtx[i][j] += lMidConfMtx
Precision = float(lConfMtx[1][1]) / (lConfMtx[1][1] + lConfMtx[1][0])
Recall = float(lConfMtx[1][1]) / (lConfMtx[1][1] + lConfMtx[0][1])
print >>OutEva,"%f\n%f" %(Precision,Recall)

OutExpTerm.close()
OutEva.close()
    