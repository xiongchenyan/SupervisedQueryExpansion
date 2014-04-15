'''
Created on Apr 15, 2014
discard the query with no eva results
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



if 4 !=len(sys.argv):
    print "target eva + to discard eva + output"
    sys.exit()
    
    
lTarget = ReadPerQEva(sys.argv[1])
lBase = ReadPerQEva(sys.argv[2])

lTargetQid = [qid for qid,measure in lTarget]

lNew = []
for item in lBase:
    if item[0] in lTargetQid:
        lNew.append(item)
    
Mean = AdhocMeasureMean([measure for qid,measure in lNew])

out = open(sys.argv[3],'w')

for item in lNew:
    print >>out, "%d\t%s" %(item[0],item[1].dumps())
    
print >>out, "mean\t%s" %(Mean.dumps())
out.close()
