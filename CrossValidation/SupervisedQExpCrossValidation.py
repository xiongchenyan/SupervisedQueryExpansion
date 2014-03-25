'''
Created on Mar 24, 2014
supervised query expansion cross validation
input: ExpTerms with labels, baseline expterm (with score)
split data to folds
for each folds:
    train-> SVM Model
    test-> CV for rest of parameters and record performance
@author: cx
'''
