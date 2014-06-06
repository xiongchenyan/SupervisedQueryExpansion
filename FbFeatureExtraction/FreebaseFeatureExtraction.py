'''
Created on Jun 6, 2014
the root class for FreebaseFeatureExtraction
to define the API's
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')


from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from IndriRelate.CtfLoader import TermCtfC
from IndriRelate.IndriInferencer import *
from cxBase.KeyFileReader import KeyFileReaderC
from base.ExpTerm import *
from FbObjCenter.FbObjCacheCenter import *
from GoogleFreebaseAPI.APIBase import *

class FreebaseFeatureExtractionC(cxBaseC):
    def Init(self):
        self.CtfCenter = TermCtfC()
        self.ObjCenter = FbObjCacheCenterC()
        self.hQObj = {} #qid ->list of FbApiObjectC
        self.QObjRankName = ""
        self.ObjRankDepth = 50
        self.Prepared = False
        self.InName = ""
        self.OutName = ""
        
    @staticmethod
    def ShowConf():
        print "termctf\nobjrank\nin\nout"
        FbObjCacheCenterC.ShowConf()
        
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        self.CtfCenter.Load(conf.GetConf('termctf'))
        self.ObjCenter.SetConf(ConfIn)
        
        self.QObjRankName = conf.GetConf('objrank')
        self.ObjRankDepth = int(conf.GetConf('objrankdepth',self.ObjRankDepth))
        
        
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        
        
    def Prepare(self):
        #inherite class add prepare data here
        if self.Prepared:
            return
        self.LoadQRankObj()  
        self.Prepared = True
        
        
    def LoadQRankObj(self):
        reader = KeyFileReaderC()
        reader.open(self.QObjRankName)
        
        for lvCol in reader:
            lQObj = []
            for vCol in lvCol[:self.ObjRankDepth]:
#                 FbObj = FbApiObjectC(vCol[2],vCol[3],float(vCol[4]))
                FbObj = self.ObjCenter.FetchObj(vCol[2])
                FbObj.SetScore(float(vCol[4]))
                lQObj.append(FbObj)
            qid = lvCol[0][0]
            lQObj = FbApiObjectC.NormalizeObjRankScore(lQObj)
            print "qid [%s]'s obj loaded" %(qid)
            self.hQObj[qid] = lQObj
        reader.close()
        return True
    
    
    
    
    def ExtractForOneQ(self,lExpTerm):
        self.Prepare()
        
        for ExpTerm in lExpTerm:
            ExpTerm = self.ExtractForOneTerm(ExpTerm)
        return lExpTerm
    
    
    def ExtractForOneTerm(self,ExpTerm):
        print "to be implemented in subclass"
        return ExpTerm
    
    
    def Process(self):
        llExpTerm = ReadQExpTerms(self.InName)
        
        out = open(self.OutName,'w')
        for lExpTerm in llExpTerm:
            lExpTerm = self.ExtractForOneQ(lExpTerm)
            for ExpTerm in lExpTerm:
                print >>out, ExpTerm.dumps()
                
        out.close()
        print "finished"
        return
    
    


        
        
        
        
        
                
        