'''
Created on Jun 23, 2014
in: expterm + feature name white list
out: expterm with only featue with name in white list
@author: chenyan
'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/QueryExpansion')


from base.ExpTerm import *
import sys

if 4 != len(sys.argv):
    print "expterm + feature white list + output"
    sys.exit()
    
    
llExpTerm = ReadQExpTerms(sys.argv[1])

hFeatureName = {}
for line in open(sys.argv[2]):
    hFeatureName[line.strip()] = True
    
out = open(sys.argv[3],'w')

for lExpTerm in llExpTerm:
    for ExpTerm in lExpTerm:
        hNew = {}
        for dim,value in ExpTerm.hFeature.items():
            if dim in hFeatureName:
                hNew[dim] = value
        ExpTerm.hFeature = hNew
        print >>out, ExpTerm.dumps()
        
out.close()
