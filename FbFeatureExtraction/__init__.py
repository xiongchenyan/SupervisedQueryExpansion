'''
extract features from Freebase for each ExpTerm

feature groups:
each group is a class
g1: from facc object ranking. as serp
    tf*idf*(normalized obj ranking score), UW with q term. DF cor with q. | at desp, and at name
    (as using obj ranking score, most terms are from top 1 obj. so that we could use top 50or1 obj)
    
g2: category KL with q: KL(p(cate|term),p(cate|q))

g3: cluster level tf, etc. not designed yet.


implementation schedule:
June 6 2014
do g1 first, and train for a results. to verify whether it will work well with current setting




'''