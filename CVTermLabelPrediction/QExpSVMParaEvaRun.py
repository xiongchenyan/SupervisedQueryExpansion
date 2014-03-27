'''
Created on Mar 26, 2014
run
@author: cx
'''


from QExpSVMParaEva import *
import sys

if len(sys.argv) < 2:
    print "1 para: conf"
    sys.exit()
    
    
QExpSVMParaEvaUnitRun(sys.argv[1])

print "finished"
