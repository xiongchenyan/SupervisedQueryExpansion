'''
Created on Aug 22, 2014
add ground truth data to expansion terms
in: expterm +_ ground truth data
output: expterm\tlabel score
@author: cx
'''

import sys

if 4 != len(sys.argv):
    print "3 para: expterm + ground truth terms + output"
    sys.exit()
    
hScore = {}

for line in open(sys.argv[2]):
    line = line.strip()
    vCol = line.split('\t')
    hScore['\t'.join(vCol[:3])] = vCol[3]
    
    
out = open(sys.argv[3],'w')
for line in open(sys.argv[1]):
    vCol = line.strip().split('\t')
    key = '\t'.join(vCol[:3])
    if key in hScore:
        print >>out, line.strip() + '\t' + hScore[key]
    else:
        print >>out, line.strip() + '\tNA'
        
out.close()



