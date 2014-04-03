'''
Created on Mar 31, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from UnsupervisedTestFoldSubmiter import *
from condor.CondorJobMonitor import CondorJobMonitorC
import sys

if 2 != len(sys.argv):
    print "1 para conf"
    UnsupervisedTestFoldSubmiterC.ShowConf()
    sys.exit()


#add a check output func
Monitor = CondorJobMonitorC()
Monitor.User = 'cx'

Monitor.Monitor() #will hold until all job finished
    
UnsupervisedTestFoldSubmiterUnitRun(sys.argv[1])
print "finished"