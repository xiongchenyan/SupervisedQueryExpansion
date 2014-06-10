'''
extract features from Freebase for each ExpTerm

feature groups:
each group is a class
g1: from facc object ranking. as serp
    tf*idf*(normalized obj ranking score), UW with q term. DF cor with q. | at desp, and at name
    (as using obj ranking score, most terms are from top 1 obj. so that we could use top 50or1 obj)
    
g2: category KL with q: KL(p(cate|term),p(cate|q))

g3: cluster level tf, etc. not designed yet.
    #not in use for now June 10

implementation schedule:
June 6 2014
do g1 first, and train for a results. to verify whether it will work well with current setting


June 10 2014:
add two group of features:
g4: query level feature, to describe whether a query should be expanded using our method
    all q-t_i share same feature for q
g5: object level feature, to describe whether a object is good for this query's expansion
    f(o) is transferred to f(t_i) via: f(t_i) = \sum_o f(o)p(o|t), p(o|t) = 1/z p(t|o).
    p(t|o) is LM probability
'''