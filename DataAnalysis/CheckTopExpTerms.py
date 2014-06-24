'''
Created on Jun 24, 2014
simply keep top exp terms for each query
in: exp term + num of top
out: result
@author: chenyan
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from base.ExpTerm import *

import sys
if 2 > len(sys.argv):
    print "2 para: expterm + num of top terms (default 10)"
    sys.exit()
    
TopN = 10
if 3 <= len(sys.argv):
    TopN = int(sys.argv[2])

llExpTerm = ReadQExpTerms(sys.argv[1])

for lExpTerm in llExpTerm:
    lExpTerm.sort(key = lambda item:item.score,reverse=True)
    for ExpTerm in lExpTerm[:TopN]:
        print ExpTerm.dumps()
    