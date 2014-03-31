'''
Created on Mar 31, 2014

@author: cx
'''

from UnsupervisedTrainFoldSubmiter import *


if 2 != len(sys.argv):
    print "1 para: conf"
    UnsupervisedTrainFoldSubmiterC.ShowConf()
    sys.exit()
    
    
UnsupervisedTrainFoldSubmiterUnitRun(sys.argv[1])
print "finished"
