'''
Created on Sep 5, 2014
Nell obj label via doc ranking score
inheritted from ObjLabelViaDocRankingScore
just use IndriExpansion (setconf)
and modify the rank object
@author: cx
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
from ObjLabel.ObjLabelViaDocRankingScore import *
from IndriExpansionBaseline.IndriExpansion import *

class NellLabelViaDocRankingScoreC(ObjLabelViaDocRankingScoreC):
    def Init(self):
        super(NellLabelViaDocRankingScoreC,self).Init()
        print "I am using Indri Expansion, so please set conf accordingly"
        self.Expander = IndriExpansionC()
        