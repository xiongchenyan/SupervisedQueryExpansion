'''
Created on May 6, 2014
select group  of features
group:
    prf
    pra
    word2vec
    hyper
@author: cx
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/TermFeatureExtraction')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')

from base.ExpTerm import *
import sys
from cxBase.base import cxConf
from copy import deepcopy
#in: exp term, out dir
#conf: all left groups
#enumerate all combination of groups
import itertools
import os,json
def KeepFeatureGroup(llExpTerm,lGroup):
    llRes = []
    for lExpTerm in llExpTerm:
        lRes = []
        for ExpTerm in lExpTerm:
            NewTerm = deepcopy(ExpTerm)
            hFeature = {}
            for feature in NewTerm.hFeature:
                Group = ExpTermC.FeatureGroup(feature)
                if Group in lGroup:
                    hFeature[feature] = NewTerm.hFeature[feature]
            NewTerm.hFeature.clear()
            NewTerm.hFeature = hFeature
            lRes.append(NewTerm)
        llRes.append(lRes)
    return llRes


def EnumrateGroup(lGroup):
    global MinGroup
    global MaxGroup
    llSubGroup = []
    for i in range(MinGroup,min(MaxGroup,len(lGroup))+1):
        lSubGroup = [list(item) for item in itertools.combinations(lGroup,i)]
        llSubGroup.extend(lSubGroup)
    return llSubGroup




if 2 != (len(sys.argv)):
    print "conf:\nin\noutdir\ngroup prf#pralvl0#pralvl1#word2vec#hyper\nmingroup\nmaxgroup"
    sys.exit()
    
conf = cxConf(sys.argv[1])
InName = conf.GetConf('in')
OutDir = conf.GetConf('outdir')
if not os.path.isdir(OutDir):
    os.makedirs(OutDir)
    
lGroup = conf.GetConf('group')
MinGroup = int(conf.GetConf('mingroup'))
MaxGroup = int(conf.GetConf('maxgroup'))


llSubGroup = EnumrateGroup(lGroup)

llExpTerm = ReadQExpTerms(InName)

for lSubGroup  in llSubGroup:
    print "working on subgroup %s" %(json.dumps(lSubGroup))
    OutName = OutDir + "/QExpTerm" + ''.join(lSubGroup)
    print "out to [%s]" %(OutName)
    llRes = KeepFeatureGroup(llExpTerm,lSubGroup)
    DumpQExpTerms(llRes,OutName)
    
print "finished"
    
    
    
    
    