'''
Created on Mar 26, 2014

@author: cx
'''


from ExpDataSpliter import *
import sys

if len(sys.argv) < 2:
    print "1 para: conf"
    sys.exit()
    
    
ExpTermDataAndParaSplitRun(sys.argv[1])
print "finished"