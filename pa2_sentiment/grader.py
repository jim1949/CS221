#!/usr/bin/python

import graderUtil
import util
import time
from util import *

grader = graderUtil.Grader()
submission = grader.load('submission')

############################################################
# Problem 1: warmup
############################################################


############################################################
# Problem 2: classification
############################################################

# Basic sanity check for feature extraction
def test2a():
    ans = {"hello":1, "world":1}
    grader.requireIsEqual(ans, submission.extractWordFeatures("hello world"))
    
grader.addBasicPart('2a-0', test2a, maxSeconds=1)   


# basic check that the classifier is working properly
def test2b():
    trainExamples = (("hello world", 1), ("goodnight moon", -1))
    testExamples = (("hello", 1), ("moon", -1))
    featureExtractor = submission.extractWordFeatures
    weights = submission.learnPredictor(trainExamples, testExamples, featureExtractor)
    grader.requireIsGreaterThan(0, weights["hello"])
    grader.requireIsLessThan(0, weights["moon"])
    
grader.addBasicPart('2b-0', test2b, maxSeconds=1)

# test the classifier on a large dataset
def test2bpolarity():
    trainExamples = readExamples('polarity.train')
    devExamples = readExamples('polarity.dev')
    featureExtractor = submission.extractWordFeatures
    weights = submission.learnPredictor(trainExamples, devExamples, featureExtractor)
    outputWeights(weights, 'weights')
    outputErrorAnalysis(devExamples, featureExtractor, weights, 'error-analysis')  # Use this to debug
    trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    devError = evaluatePredictor(devExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
    print "Official: train error = %s, dev error = %s" % (trainError, devError)
    grader.requireIsLessThan(0.08, trainError)
    grader.requireIsLessThan(0.30, devError)

grader.addBasicPart('2b-1', test2bpolarity, maxSeconds=7)
    

# Check that a positively labelled example is classified positively, and negative examples are negative.
def test2c():
    weights = {"hello":1, "world":1}
    data = submission.generateDataset(5, weights)
    for datapt in data:
        grader.requireIsEqual((util.dotProduct(datapt[0], weights) >= 0), (datapt[1] == 1))

grader.addBasicPart('2c-0', test2c, maxSeconds=1)


############################################################

grader.addManualPart('2d', 4)
grader.addManualPart('2e', 3)

# sanity check for this feature function
def test2f():
    fe = submission.extractCharacterFeatures(3)
    sentence = "hello world"
    ans = {"hel":1, "ell":1, "llo":1, "low":1, "owo":1, "wor":1, "orl":1, "rld":1}
    grader.requireIsEqual(ans, fe(sentence))

grader.addPart('2f-0', test2f, maxSeconds=1)


grader.addManualPart('2g', 3)

grader.addManualPart('2h', 5, extraCredit=True)

############################################################
# Problem 3: clustering
############################################################

grader.addManualPart('3a', 5)

# basic test for k-means
def test3b():
    x1 = {0:0, 1:0}
    x2 = {0:0, 1:1}
    x3 = {0:0, 1:2}
    x4 = {0:0, 1:3}
    x5 = {0:0, 1:4}
    x6 = {0:0, 1:5}
    examples = [x1, x2, x3, x4, x5, x6]
    centers, assignments, totalCost = submission.kmeans(examples, 2, maxIters=10)
    # (there are two stable centroid locations)
    grader.requireIsEqual(True, totalCost==4 or totalCost==5.5)
    
grader.addBasicPart('3b-0', test3b, maxSeconds=1)


grader.addManualPart('3c', 5)

grader.grade()
