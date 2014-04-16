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

if 2 < len(sys.argv):
    print "1 para conf (2 para then the second one is 1:wait for condor job 0:direct submit"
    UnsupervisedTestFoldSubmiterC.ShowConf()
    sys.exit()


#add a check output func
WaitBool = True
if len(sys.argv) > 2:
    WaitBool = bool(int(sys.argv[2]))
if WaitBool:
    Monitor = CondorJobMonitorC()
    Monitor.User = 'cx'
    Monitor.Monitor() #will hold until all job finished
    
UnsupervisedTestFoldSubmiterUnitRun(sys.argv[1])
print "finished"