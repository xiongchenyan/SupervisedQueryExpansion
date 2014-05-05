'''
Created on Apr 29, 2014
merge edge feature to term PRA feature
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/QueryFreebaseSemantic')
from base.ExpTerm   import *
from EdgeFeature.EdgeFeatureBase import EdgeFeatureC
from cxBase.base import cxConf,cxBaseC


'''
read EdgeFeture to HFeature from Edge files
read exp term one by one, 
    for each feature
        get its type
        extract hyper feature value, and record to hEdgeTypeHyper[]={max,min,mean,cnt}
        decide whether to keep this raw feature
    merge hype feature value
    output   
'''


class TermPRAHyperFeatureMergerC(cxBaseC):
    def Init(self):
        self.TermIn = ""
        self.OutName = ""
        self.lEdgeFeature = []
        self.hEdgeFeature = {}
        
        self.KeepPRFFeature = True
        self.KeepPRALvl1Feature = True
        self.KeepPRALvl2Feature = True
        
        self.EdgeTypeGrouping = 'lvltype' 
        #how to group edge type:
            #lvl: only lvl
            #lvltype: lvl+type
            #type: type only
            #one: everything in one group
            #lvl-type-domain: add domain as path type 
        
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.lEdgeFeature = conf.GetConf('edgefeature', self.lEdgeFeature)
        self.KeepPRFFeature = bool(int(conf.GetConf('keepprf',1)))
        self.KeepPRALvl1Feature = bool(int(conf.GetConf('keeplvl1',1)))
        self.KeepPRALvl2Feature = bool(int(conf.GetConf('keeplvl2',0)))
        self.OutName = conf.GetConf('out')
        self.TermIn = conf.GetConf('in')
        self.EdgeTypeGrouping = conf.GetConf('edgetypegrouping',self.EdgeTypeGrouping)
        
    @staticmethod
    def ShowConf():
        print "edgefeature\nkeepprf\nkeeplvl1\nkeeplvl2\nin\nout\nedgetypegrouping lvltype"   
        
        
    def Process(self):
        print "start read edge features"
        for EdgeFeatureIn in self.lEdgeFeature:
            self.hEdgeFeature= EdgeFeatureC().LoadFeatureToDict(EdgeFeatureIn,self.hEdgeFeature)
        print "read edge feature finished"
        
        out = open(self.OutName,'w')
        for line in open(self.TermIn):
            ExpTerm = ExpTermC(line.strip())
            ExpTerm = self.ProcessOneTerm(ExpTerm)
            print >> out,ExpTerm.dump()
        out.close()
        print "finished"
        return True
    
    def ProcessOneTerm(self,ExpTerm):
        
        hNewFeature = {}
        hMergeHyperFeature = {} #type+dim->value
        
        for feature in ExpTerm.hFeature:
            value = ExpTerm.hFeature[feature]
            if self.KeepFeature(feature):
                print "keep feature [%s]" %(feature)
                hNewFeature[feature] = value
            else:
                print "discard feature [%s]" %(feature)
            
            FeatureType = ExpTermC().PRAFeatureType(feature,self.EdgeTypeGrouping)
            if FeatureType == 'prf':
                continue
            
            lhThisHyperFeature = self.FetchHyperFeature(feature)
            
            self.MergeHyperFeature(lhThisHyperFeature,hMergeHyperFeature,FeatureType)              
        
        
        #filter feature
        ExpTerm.hFeature = hNewFeature
        
        hToAddFeature = self.TransferFeatureStatToFeature(hMergeHyperFeature)
        
        ExpTerm.AddFeature(hToAddFeature)        
        
        return ExpTerm
    
    
    def TransferFeatureStatToFeature(self,hMergeHyperFeature):
        hToAddFeature = {}
        
        for item in hMergeHyperFeature:
            l = hMergeHyperFeature[item]
            hToAddFeature[item + 'Max'] = l[0]
            hToAddFeature[item + 'Min'] = l[1]
            hToAddFeature[item + 'Mean'] = l[2]
            hToAddFeature[item + 'Cnt'] = l[3]
            
        return hToAddFeature
        
        
    
    def KeepFeature(self,feature):
        FeatureType = ExpTermC().PRAFeatureType(feature)
        print "type [%s]" %(FeatureType)
        if FeatureType == 'prf':
            return  self.KeepPRFFeature
        vCol = FeatureType.split('-')
        if len(vCol) == 1:
            return self.KeepPRALvl1Feature
        if len(vCol) == 2:
            return self.KeepPRALvl2Feature
        return False
    
    def FetchHyperFeature(self,feature):
        lhFeature = []
        
        #break feature to edges
        #discard stopedge
        #for each edges, load the hyper features
        #
        lEdge = SegEdgeFromPRAFeature(feature,True)
#         print "fetching hyper feature for [%s]" %(feature)
        for edge in lEdge:
            if edge in self.hEdgeFeature:
#                 print "edge [%s] has [%s]" %(edge,self.hEdgeFeature[edge].dumps())
                lhFeature.append(self.hEdgeFeature[edge].hFeature)
        
        return lhFeature    
    
    def MergeHyperFeature(self,lhThisHyperFeature,hMergeHyperFeature,FeatureType):
        
        for hFeature in lhThisHyperFeature:
            for DimName in hFeature:
                value = hFeature[DimName]
                key = FeatureType + DimName
                if not key in hMergeHyperFeature:
                    hMergeHyperFeature[key] = [value,value,value,1.0] #'max,min,mean,cnt'
                else:
                    MaxValue,MinValue,MeanValue,Cnt = hMergeHyperFeature[key]
                    MaxValue = max(MaxValue,value)  
                    MinValue = min(MinValue,value)
                    MeanValue = (MeanValue * Cnt +value) /(1.0 + Cnt)
                    Cnt += 1
                    hMergeHyperFeature[key] = [MaxValue,MinValue,MeanValue,Cnt]
        return    
    
    
    

