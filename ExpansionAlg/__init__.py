'''
the expansion algorithm used in the paper
input: term with score (in), baseline term scores (baseterm), parameters (para set)
do: merge term score with baseline term score, with given parameter, generate final q terms
    re-rank
    evaluate
output:
    evaluate results:
        one file for per query
        one file for mean
very similar with exp unit run in query expansion
    input and output format try to be the same as possible,
    thus can use same train/test cv submiter
        and same eva results collector
'''



'''
detailed design:
1: a expansion like class: in: scored term + base term + para => merged q terms (same as IndriExpansion)
2: re-orgenize the ExpansionSingleRunPipe, make it cleaner and suitable for cv-submit needs

'''