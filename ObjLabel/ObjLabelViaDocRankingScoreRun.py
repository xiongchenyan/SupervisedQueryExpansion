'''
Created on Aug 22, 2014
run it!
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')

from ObjLabel.ObjLabelViaDocRankingScore import *
import sys

if len(sys.argv) != 2:
    print "conf:"
    ObjLabelViaDocRankingScoreC.ShowConf()
    sys.exit()
    
Runner  = ObjLabelViaDocRankingScoreC(sys.argv[1])
Runner.Process()
