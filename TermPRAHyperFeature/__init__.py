'''
merge edge level hyper feature to path level
input: exp term with pra feature
        + edge features
output: exp term with PRA feature + edge merged to path hyper feature
the PRA feature could be filtered by configure


merging:
    4 lvl information: max, min, mean, cnt
    merge to path type: (first version: (cotype,neighbor,~)^2~= 6 type)
    total |path type| * |4 lvl| = 24 dimension    
'''