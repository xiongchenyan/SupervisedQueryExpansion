'''
Created on Mar 26, 2014
run
@author: cx
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
from QExpSVMTestFoldSubmiter import QExpSVMTestFoldSubmiterC
from condor.CondorJobMonitor import CondorJobMonitorC
import sys

if len(sys.argv) < 2:
    print "1 para: conf"
    QExpSVMTestFoldSubmiterC.ShowConf()
    sys.exit()


#add a check output func
WaitBool = True
if len(sys.argv) > 2:
    WaitBool = bool(int(sys.argv[2]))
if WaitBool:
    Monitor = CondorJobMonitorC()
    Monitor.User = 'cx'
    Monitor.Monitor() #will hold until all job finished
    
Submiter = QExpSVMTestFoldSubmiterC(sys.argv[1])

lJob = Submiter.Process()

print "finished, submit jobs:\n%s" %('\n'.join(lJob))
