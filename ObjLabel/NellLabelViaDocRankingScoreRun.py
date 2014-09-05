'''
Created on Sep 5, 2014
run
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from ObjLabel.NellLabelViaDocRankingScore import *
import sys

if len(sys.argv) != 2:
    print "conf:"
    NellLabelViaDocRankingScoreC.ShowConf()
    sys.exit()
    
Runner  = NellLabelViaDocRankingScoreC(sys.argv[1])
Runner.Process()

