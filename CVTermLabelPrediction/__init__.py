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
    partitioning data to train_dev_test folds (a sub class or partition)
    make parameter files (direct call lib)
    make a condor submit file that:
        submit a job for each train-dev-para combination 
            to be implemented as a sub class of SVMRunSinglePara
        automatic submit
            call lib in condor submit part
    --here we need a manually hold (or we could hold a monitor process, to wait for all job complete)---
        for now manually do it. after a while see if we can do it automatically
    collect all dev performance, select the best para
    apply on test and get result (accuracy and prediction label)
'''