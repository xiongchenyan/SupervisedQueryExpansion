'''
Created on Mar 26, 2014
run
@author: cx
'''

from QExpSVMTestFoldSubmiter import *

import sys

if len(sys.argv) < 2:
    print "1 para: conf"
    QExpSVMTestFoldSubmiterC.ShowConf()
    sys.exit()
    
Submiter = QExpSVMTestFoldSubmiterC(sys.argv[1])

lJob = Submiter.Process()

print "finished, submit jobs:\n%s" %(['\n'].join(lJob))
