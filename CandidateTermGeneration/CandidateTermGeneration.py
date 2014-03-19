'''
Created on Mar 18, 2014
father class for candidate term generation
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/local/lib/python2.7/site-packages')
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
from IndriRelate.IndriPackedRes import *
from cxBase.base import *
class CandidateTermGenerationC(object):
    
    def Init(self):
        return
    
    def SetConf(self,ConfIn):
        return
    
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
        return
    

             
        
 