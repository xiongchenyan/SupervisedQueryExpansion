'''
Created on Jun 6, 2014
        #feature to extract:
            #FbPrfTfIdfName
            #FbPrfTfIdfDesp
            #FbPrfTfUwQName
            #FbPrfTfUwQDesp
            #FbPrfTfUwBiQName
            #FbPrfTfUwBiQDesp
            #FbPrfDfCorName
            #FbPrfDfCorDesp
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from FbFeatureExtraction.FreebaseFeatureExtraction import *

from cxBase.TextBase import *

class FreebasePrfFeatureExtractionC(FreebaseFeatureExtractionC):
    
    def ExtractForOneTerm(self,ExpTerm):

        print "extracting FbPrf [%s][%s]-[%s]" %(ExpTerm.qid,ExpTerm.query,ExpTerm.term)
        
        lFaccObj = []
        lGoogleObj = []
        if ExpTerm.qid in self.hQFaccObj:
            lFaccObj = self.hQFaccObj[ExpTerm.qid]
        if ExpTerm.qid in self.hQGoogleObj:
            lGoogleObj = self.hQGoogleObj[ExpTerm.qid]
        
        llObj = [lFaccObj,lGoogleObj]
        lPre = ['Facc','Google']
        lField = ['Name','Desp']
        
        for field in lField:
            for i in range(len(llObj)):
                lObj = llObj[i]
                if [] == lObj:
                    continue
                pre = lPre[i] 
                self.ExtractTfIdf(ExpTerm,field,lObj,pre)        
                self.ExtractTfUwQ(ExpTerm,field,lObj,pre)
                self.ExtractTfUwBiQ(ExpTerm,field,lObj,pre)
                self.ExtractDfCor(ExpTerm,field,lObj,pre)
            
        return ExpTerm
    
    def GetObjField(self,Obj,field):
        if field == 'Name':
            text = Obj.GetName()
        else:
            text = Obj.GetDesp()
        text = TextBaseC.RawClean(text)
        return text
    
    def ExtractTfIdf(self,ExpTerm,field,lObj,pre):
        Feature = 'Fb%sPrfTfIdf' %(pre) + field
        value = 0
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            Lm = LmBaseC(text)
            value += Lm.GetTF(ExpTerm.term) * self.CtfCenter.GetLogIdf(ExpTerm.term) * Obj.GetScore()
        
        ExpTerm.hFeature[Feature] = value
        
        
    
        
    def ExtractTfUwQ(self,ExpTerm,field,lObj,pre):
        Feature = 'Fb%sPrfTfUwQ' %(pre) + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            for qterm in ExpTerm.query.split():
                lTerm = [qterm,ExpTerm.term]
                value += TextBaseC.UW(text.split(), lTerm)
        ExpTerm.hFeature[Feature] = value
        
    def ExtractTfUwBiQ(self,ExpTerm,field,lObj,pre): 
        Feature = 'Fb%sPrfTfUwBiQ'%(pre) + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            lQTerm = ExpTerm.query.split()
            for i in range(len(lQTerm) - 1):
                lTerm = [lQTerm[i],lQTerm[i+1],ExpTerm.term]
                value += TextBaseC.UW(text.split(), lTerm)
        ExpTerm.hFeature[Feature] = value    
        
    def ExtractDfCor(self,ExpTerm,field,lObj,pre):
        Feature = 'Fb%sPrfDfCor' %(pre) + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            Cor = 0
            for term in ExpTerm.query.split():
                if (term in text) & (ExpTerm.term in text):
                    Cor = 1
                    break
            value += Cor
        ExpTerm.hFeature[Feature] = value
        
        

#     
# import sys
# if 2 != len(sys.argv):
#     print "conf"
#     FreebasePrfFeatureExtractionC.ShowConf()
#     sys.exit()
#     
# Extractor = FreebasePrfFeatureExtractionC(sys.argv[1])
# Extractor.Process()


