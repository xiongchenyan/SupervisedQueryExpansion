'''
Created on Sep 2, 2014
plot the query difficulty (err) Vs relative performance of each query
@author: cx
'''


from cxBase.base import cxConf
from ResultAnalysis.AdhocResAnalysis import AdhocResAnalysisC


import sys


if 2 != len(sys.argv):
    print "1 conf\nout"
    AdhocResAnalysisC().ShowConf()
    sys.exit()
    
Analysiser = AdhocResAnalysisC(sys.argv[1])

conf = cxConf(sys.argv[1])
caption = conf.GetConf('caption')
OutName = conf.GetConf('out')


Analysiser.PlotPerformVsBaseDifficulty(OutName)

print "done"