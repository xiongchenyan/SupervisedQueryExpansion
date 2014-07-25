'''
Created on Jul 25, 2014
get the most helped and hurt query
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from ResultAnalysis.AdhocResAnalysis import *

from cxBase.Conf import cxConfC

import sys

if 2 != len(sys.argv):
    print '1 conf:'
    AdhocResAnalysisC.ShowConf()
    print 'query\ntoanamethod'
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])
Analysiser = AdhocResAnalysisC(sys.argv[1])

QInName = conf.GetConf('query')
lMethodName = conf.GetConf('toanamethod')

hQuery = {}
for line in open(QInName):
    qid,query = line.strip().split('\t')
    hQuery[int(qid)] = query
    
Analysiser.MostWinLoss(lMethodName, hQuery)