'''
Created on Mar 31, 2014
run prediction per fold
@author: cx
'''



from QExpSVMPerFoldPrediction import *

if 2 != len(sys.argv):
    print "1 conf"
    sys.exit()
    
    
QExpSVMPerFOldPredictorRun(sys.argv[1])
print "finished"