'''
Created on Jul 22, 2014

@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from TermLabel.TermLabelViaDocRankingScore import *
import sys

if 2 != len(sys.argv):
    print "conf"
    TermLabelViaDocRankingScoreC.ShowConf()
    sys.exit()
    
Evaluator = TermLabelViaDocRankingScoreC(sys.argv[1])
Evaluator.Process()
print "done"
            
            
        