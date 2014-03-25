'''
from expansion terms (feature + label), to predicted expansion terms'
input:
    expansion term
    kinds of different sources
    K
    working folder
output:
    average accuracy
    expansion term with predict labels
'''


'''
cause need to parallel, so this get very tricky
general work flow:
    partitioning data to train_dev_test folds
    make parameter files
    make a condor submit file that:
        submit a job for each train-dev-para combination
        automatic submit
    --here we need a manually hold (or we could hold a monitor process, to wait for all job complete)---
    collect all dev performance, select the best para
    apply on test and get result (accuracy and prediction label)
    

'''