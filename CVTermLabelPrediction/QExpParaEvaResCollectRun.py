'''
Created on Mar 27, 2014

@author: cx
'''

from QExpParaEvaResCollect import *

import sys

if 2 > len(sys.argv):
    print "1 para: conf"
    sys.exit()
    
    
QExpParaEvaResCollectorUnitTest(sys.argv[1])



