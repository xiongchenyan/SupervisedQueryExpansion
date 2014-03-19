'''
Created on Mar 18, 2014

@author: cx
'''

from TrainingDataFromSERP import *

import sys

if 2 != len(sys.argv):
    print "1 para conf:\nin\nout"
    sys.exit()
    
    
Pipe = TrainingDataFromSERPC(sys.argv[1])
conf = cxConf(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')

Pipe.Process(InName, OutName)

print "done"