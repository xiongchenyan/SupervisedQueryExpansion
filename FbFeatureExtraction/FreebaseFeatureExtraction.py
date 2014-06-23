'''
Created on Jun 6, 2014
the root class for FreebaseFeatureExtraction
to define the API's
@author: cx
'''

'''
June 6.11:
load facc obj rank and google obj rank as the same time, and all features are
extracted from both ranks
require change on all sub classes
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
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
#         self.hQObj = {} #qid ->list of FbApiObjectC
        
        self.hQFaccObj = {}
        self.hQGoogleObj = {}
        
        
#         self.QObjRankName = ""
        self.QFaccObjRankName = ""
        self.QGoogleObjRankName = ""
        
        
        self.ObjRankDepth = 10
#         self.Prepared = False
        self.InName = ""
        self.OutName = ""
        
    @staticmethod
    def ShowConf():
        print "termctf\nfaccrank\ngooglerank\nin\nout"
        FbObjCacheCenterC.ShowConf()
        
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        self.CtfCenter.Load(conf.GetConf('termctf'))
        self.ObjCenter.SetConf(ConfIn)
        
#         self.QObjRankName = conf.GetConf('objrank')
        
        self.QFaccObjRankName = conf.GetConf('faccrank')
        self.QGoogleObjRankName = conf.GetConf('googlerank')
        
        self.ObjRankDepth = int(conf.GetConf('objrankdepth',self.ObjRankDepth))
        
        
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
        
        
    def Prepare(self,qid,query):
        #inherite class add prepare data here
#         if self.Prepared:
#             return
        if ({} == self.hQFaccObj) | ({} == self.hQGoogleObj):
            self.LoadQRankObj()
        
        self.hQFaccObj = self.FillForQ(qid, self.hQFaccObj)
        self.hQGoogleObj = self.FillForQ(qid, self.hQGoogleObj)
        
#         self.Prepared = True
    
    
    def FillForQ(self,qid,hQObj):
        if qid in hQObj:
            #fill a qid's obj only when needed
            lQObj = hQObj[qid]
            
            #score must be manually kept....
            for i in range(len(lQObj)):
                score = lQObj[i].GetScore()
                name = lQObj[i].GetName()
                lQObj[i] = self.ObjCenter.FetchObj(lQObj[i].GetId())
                lQObj[i].SetScore(score)
                lQObj[i].SetName(name.lower())
            
            hQObj[qid] = lQObj
        return hQObj
        
        
    def LoadQRankObj(self):
        self.hQFaccObj = self.LoadQRankObjFromFile(self.QFaccObjRankName)
        self.hQGoogleObj = self.LoadQRankObjFromFile(self.QGoogleObjRankName)
    
    
    def LoadQRankObjFromFile(self,QObjRankName):
        if '' == QObjRankName:
            return {}
        reader = KeyFileReaderC()
        reader.open(QObjRankName)
        hQObj = {}
        for lvCol in reader:
            lQObj = []
            for vCol in lvCol[:self.ObjRankDepth]:
                FbObj = FbApiObjectC(vCol[2],vCol[3],float(vCol[4]))
#                 FbObj = self.ObjCenter.FetchObj(vCol[2])
#                 FbObj.SetScore(float(vCol[4]))
                lQObj.append(FbObj)
            qid = lvCol[0][0]
            lQObj = FbApiObjectC.NormalizeObjRankScore(lQObj)
#             print "qid [%s]'s obj loaded" %(qid)
            hQObj[qid] = lQObj
        print "q rank obj loaded from [%s]" %(QObjRankName)
        reader.close()
        return hQObj
    
    
    
    def ExtractForOneQ(self,lExpTerm):
        self.Prepare(lExpTerm[0].qid,lExpTerm[1].query)        
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
    
    


        
        
        
        
        
                
        