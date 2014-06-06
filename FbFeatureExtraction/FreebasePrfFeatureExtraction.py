'''
Created on Jun 6, 2014

@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/cxPylib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from FbFeatureExtraction.FreebaseFeatureExtraction import *


class FreebasePrfFeatureExtractionC(FreebaseFeatureExtractionC):
    
    def ExtractForOneTerm(self,ExpTerm):
        #feature to extract:
            #FbPrfTfIdfName
            #FbPrfTfIdfDesp
            #FbPrfTfUwQName
            #FbPrfTfUwQDesp
            #FbPrfTfUwBiQName
            #FbPrfTfUwBiQDesp
            #FbPrfDfCorName
            #FbPrfDfCorDesp
        if not ExpTerm.qid in self.hQObj:
            return    
            
        self.ExtractTfIdf(ExpTerm,'Name')
        self.ExtractTfIdf(ExpTerm,'Desp')        
        self.ExtractTfUwQ(ExpTerm,'Name')
        self.ExtractTfUwQ(ExpTerm,'Desp')
        self.ExtractTfUwBiQ(ExpTerm,'Name')
        self.ExtractTfUwBiQ(ExpTerm,'Desp')
        self.ExtractDfCor(ExpTerm,'Name')
        self.ExtractDfCor(ExpTerm,'Desp')
        
        return ExpTerm
    
    def GetObjField(self,Obj,field):
        if field == 'Name':
            text = Obj.GetName()
        else:
            text = Obj.GetDesp()
        return text
    
    def ExtractTfIdf(self,ExpTerm,field):
        lObj = self.hQObj[ExpTerm.qid]
        Feature = 'FbPrfTfIdf' + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            Lm = LmBaseC(text)
            value += Lm.GetTF(ExpTerm.term) * self.CtfCenter.GetLogIdf(ExpTerm.term) * Obj.GetScore()
        
        ExpTerm.hFeature[Feature] = value
        
        
    
        
    def ExtractTfUwQ(self,ExpTerm,field):
        lObj = self.hQObj[ExpTerm.qid]
        Feature = 'FbPrfTfUwQ' + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            for qterm in ExpTerm.query.split():
                lTerm = [qterm,ExpTerm.term]
                value += TextBaseC.UW(text.split(), lTerm)
        ExpTerm.hFeature[Feature] = value
        
    def ExtractTfUwBiQ(self,ExpTerm,field): 
        lObj = self.hQObj[ExpTerm.qid]
        Feature = 'FbPrfTfUwBiQ' + field
        value = 0
        
        for Obj in lObj:
            text = self.GetObjField(Obj, field)
            lQTerm = ExpTerm.query.split()
            for i in range(len(lQTerm) - 1):
                lTerm = [lQTerm[i],lQTerm[i+1],ExpTerm.term]
                value += TextBaseC.UW(text.split(), lTerm)
        ExpTerm.hFeature[Feature] = value    
        
    def ExtractDfCor(self,ExpTerm,field):
        lObj = self.hQObj[ExpTerm.qid]
        Feature = 'FbPrfDfCor' + field
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
        
        



