'''
Created on Apr 1, 2014
run
@author: cx
'''

from ExpansionSingleRunCenter import *


import sys


if 2 != len(sys.argv):
    print "1 para: conf\n"
    ExpansionSingleRunCenterC.ShowConf()
    sys.exit()
    
    
SingleRunPipe = ExpansionSingleRunCenterC(sys.argv[1])
SingleRunPipe.Process()

print "finished"