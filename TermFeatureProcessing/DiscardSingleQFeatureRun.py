'''
Created on May 5, 2014

@author: cx
'''




import sys
import site
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from DataAnalysis.CalcFeatureQueryCnt import *
from base.ExpTerm import ExpTermC,ReadQExpTerms
from TermFeatureProcessing.DiscardSingleQFeature import DiscardSingleQFeature
if 3 != len(sys.argv):
    print "2 para: input exp term + output term with filered feature"
    sys.exit()


llExpTerm = ReadQExpTerms(sys.argv[1])
    
llExpTerm = DiscardSingleQFeature(llExpTerm)    
out = open(sys.argv[2],'w')

for lExpTerm in llExpTerm:
    for ExpTerm in lExpTerm:
        print >>out, ExpTerm.dump()
out.close()

print "finished"