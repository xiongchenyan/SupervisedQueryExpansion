'''
Created on Sep 9, 2014
fetch fb svm and fb cat from FbFeature in
in FbFeature + outname + type(fbsvm|fbcat)
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/SupervisedQueryExpansion')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from base.ExpTerm import *
import sys






if 4 !=len(sys.argv):
    print '3 para:FbFeature + output + fbsvm|fbcat'
    sys.exit()
    
    
llExpTerm = ReadQExpTerms(sys.argv[1])

lTargetFeature = ['FbFaccPrfTfIdfDesp','FbGooglePrfTfIdfDesp','QTermCateKL']


out = open(sys.argv[2],'w')

if sys.argv[3] == 'fbcat':
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            if not lTargetFeature[2] in ExpTerm.hFeature:
                continue
            ExpTerm.score = ExpTerm.hFeature[lTargetFeature[2]]
            ExpTerm.hFeature = {}
            print >>out, ExpTerm.dumps()
            
else:
    for lExpTerm in llExpTerm:
        for ExpTerm in lExpTerm:
            hNew = {}
            for key,item in ExpTerm.hFeature.items():
                if key in lTargetFeature:
                    hNew[key] = item
            ExpTerm.hFeature = hNew
            print >>out, ExpTerm.dumps()
            
out.close()

print "finished"