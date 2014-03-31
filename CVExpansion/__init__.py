'''
cross validation for query expansion.
a super virtual class.
    the basic framework for submitting jobs for CV (implemented in GeekTool CV)
and inheritive classes, as in this package:
    RMExp
    MixExp
    Supervised Exp, with given score
with per fold runs of
    RMExp, MixExp (implemented in QueryExpansion project)
    ScoreExp (implemented here)
'''