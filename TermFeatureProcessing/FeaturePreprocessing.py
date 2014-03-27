'''
Created on Mar 27, 2014
do:
    binarize label
    feature -> init name

@author: cx
'''



import site
import pickle

site.addsitedir('/bos/usr0/cx/PyCode/Geektools')
site.addsitedir('/bos/usr0/cx/PyCode/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
from cxBase.base import *
from FeatureHash import *


import sys


if 1 > len(sys.argv):
    print "1 para: conf file"
    print "in\nout\nfeaturenamedict"
    sys.exit()
    
conf = cxConf()