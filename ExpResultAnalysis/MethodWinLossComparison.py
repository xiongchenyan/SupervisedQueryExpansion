'''
Created on Jul 7, 2014
compare methods' by win/loss/tie number
input: same as AdhocResAnalysis class + a list of to evaluation method name (must be in AdhocResAnalysis's)
output: a table showing win loss tie comparison
@author: chenyan
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxConf
from ResultAnalysis.AdhocResAnalysis import AdhocResAnalysisC
import sys

if 2 != len(sys.argv):
    print "conf:"
    AdhocResAnalysisC.ShowConf()
    print "winlosscompmethodname\nout"
    sys.exit()
    
    
conf = cxConf(sys.argv[1])

lEvaMethodName = conf.GetConf('winlosscompmethodname')
if type(lEvaMethodName) != list:
    lEvaMethodName = [lEvaMethodName]
OutName = conf.GetConf('out')

Center = AdhocResAnalysisC(sys.argv[1])

TableStr = Center.WinLossTieTable(lEvaMethodName)

out = open(OutName,'w')
print >>out, TableStr
out.close()
print "finished"

    
