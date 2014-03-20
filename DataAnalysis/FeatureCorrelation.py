'''
Created on Mar 20, 2014
pearson of feature and label
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
import json

import sys


if 3 != len(sys.argv):
    print "term features in + out"
    sys.exit()
    
lExpTerm = []
for line in open(sys.argv[1]):
    line = line.strip()
    ExpTerm = ExpTermC(line)
    lExpTerm.append(ExpTerm)
    
hFeatureCoor = FeatureCorrelationAnalysis(lExpTerm)
out = open(sys.argv[2],'w')
print >>out,json.dumps(hFeatureCoor,indent=1)
out.close()