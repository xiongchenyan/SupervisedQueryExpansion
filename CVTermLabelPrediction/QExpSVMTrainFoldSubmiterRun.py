'''
Created on Mar 26, 2014

@author: cx
'''

from QExpSVMTrainFoldSubmiter import *

import sys

if len(sys.argv) < 2:
    print "1 para conf"
    QExpSVMTrainFoldSubmiterC.ShowConf()
    sys.exit()
    
    
Submiter = QExpSVMTrainFoldSubmiterC(sys.argv[1])
lJob = Submiter.Process()

print "submitted:\n%s" %(json.dumps(lJob,indent=1))


