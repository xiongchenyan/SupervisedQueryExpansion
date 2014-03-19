'''
Created on Mar 18, 2014
generate from SERP
same as Guihong's paper
@author: cx
'''

from CandidateTermGeneration import *



class CandidateTermFromSERPC(CandidateTermGenerationC):
    
    def Init(self):
        super(CandidateTermFromSERPC,self).Init()
        self.CashDir = ""
        self.NumOfSERPDoc = 20
        self.MinFilterCnt = 3
        return
    
    def SetConf(self,ConfIn):
        super(CandidateTermFromSERPC,self).SetConf(ConfIn)
        print "sub classes's set conf called successfully"
        conf = cxConf(ConfIn)
        self.CashDir = conf.GetConf("cashdir")
        self.NumOfSERPDoc = int(conf.GetConf('numofserpdoc'))
        self.MinFilterCnt = int(conf.GetConf('minfiltercnt'))
        return True
    
    
    
    
    def ExtractFromDoc(self,doc):
        hTerm = {}
        for term in doc.GetContent().split():
            if '[oov]' == term.lower():
                continue
            if not term in hTerm:
                hTerm[term] = 0
            hTerm[term] += 1
        return hTerm
    
    def FilterTerm(self,hTerm):
        hRes = {}
        for item in hTerm:
            if hTerm[item] > self.MinFilterCnt:
                hRes[item] = hTerm[item]
        return hRes
    
    def Process(self,query,lDoc = []):
        if [] == lDoc:
            lDoc = ReadPackedIndriRes(self.CashDir + "/" + query,self.NumOfSERPDoc)
        else:
            lDoc = lDoc[:self.NumOfSERPDoc]
        hTerm = {}
        for doc in lDoc:
            hMid = self.ExtractFromDoc(doc)
            hTerm = dict(hTerm.items() + hMid.items())
        hTerm = self.FilterTerm(hTerm)
        return hTerm.keys()
    
    
    
def CandidateTermFromSERPUnitTest(ConfIn):
    print "in\nout\ncashdir\nnumofserpdoc 20\nminfiltercnt 3\n"
    
    conf = cxConf(ConfIn)
    InName = conf.GetConf("in")
    OutName = conf.GetConf("out")
    CandidateTermFromSERP = CandidateTermFromSERPC(ConfIn)
    
    out = open(OutName,'w')
    for line in open(InName):
        qid,query= line.strip().split('\t')
        lTerm = CandidateTermFromSERP.Process(query)
        for term in lTerm:
            print >> out,qid + '\t' + query + '\t' + term
    out.close()
    return True
    
            
        
        