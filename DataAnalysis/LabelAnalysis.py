'''
Created on Mar 20, 2014
check the label distribution "term performance"
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from ResultAnalysis.ScoreBin import *
from base.ExpTerm import *
import sys
import json
if 3 != len(sys.argv):
    print "2 para: expansion term in + bin label score output"
    sys.exit()
    
    
BinNum = 20
lScore = []
for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    lScore.append(ExpTerm.score)

print "read score:\n%s" %(json.dumps(lScore,indent=1))    
lBin = BinValue(lScore,BinNum)
print "bin res\n %s" %(json.dumps(lBin,indent=1))
out = open(sys.argv[2],'w')
print >> out,json.dumps(lBin,indent=1)
out.close()


