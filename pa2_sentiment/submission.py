#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *
from time import time
import itertools
from numpy import average

############################################################
# Problem 2: binary classification
############################################################

############################################################
# Problem 2a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    a = Counter(x.split())
    return dict(a)
    # END_YOUR_CODE

# print extractWordFeatures("I am what I am")
############################################################
# Problem 2b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned.

    You should implement stochastic gradient descent.


    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    
    'an ultra-low-budget indie debut that smacks more of good intentions than talent', -1
    
    things to take care:
        feature extraction
        loss function
        SGD
        generality
    '''
    # BEGIN_YOUR_CODE (around 15 lines of code expected)

    weights = {}  # feature => weight
    eta = 0.01
    numIters = 20
    extractedTrainExamples = [(featureExtractor(x), y) for x, y in trainExamples]
    extractedTestExamples = [(featureExtractor(x), y) for x, y in testExamples]
    for i in range(numIters): #epochs
        for (phi, y) in extractedTrainExamples: # iterate over all the examples
            if(1 - dotProduct(weights, phi) * y > 0):  #cost function is max(0, 1-dot(weights, phi))
                increment(weights, eta * y, phi)  #gradient is -phi*y  , so all we need is a cost function value and its gradient

        # trainError = evaluatePredictor(extractedTrainExamples, lambda(x) : (1 if dotProduct(x, weights) >= 0 else -1))
        # devError = evaluatePredictor(extractedTestExamples, lambda(x) : (1 if dotProduct(x, weights) >= 0 else -1))
        # print 'iteration %d, trainError=%f, devError=%f' % (i, trainError, devError)
    # END_YOUR_CODE
    return weights

############################################################
# Problem 2c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) can be anything (randomize!) with a nonzero score under the given weight vector
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        phi = {}
        for x in weights.keys():
            num = random.randint(-10, 10)
            if (num > 0):
                phi[x] = num
        y = 1 if dotProduct(phi, weights) >= 0 else -1
        # END_YOUR_CODE
        return (phi, y)
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 2f: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        word = "".join(x.split())
        dic = {}
        for i in range(len(word) + 1 - n):
            ngram = word[i:i + n]
            dic[ngram] = dic.get(ngram, 0) + 1
        return dic
        # END_YOUR_CODE
    return extract

############################################################
# Problem 2h: extra credit features

def extractExtraCreditFeatures(x):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    x = x.replace('-', ' ')
    x = x.replace('.', ' ')
    x = x.replace(',', ' ')
    x = x.replace('\'', ' ')

    dic = {}
    flag = 0
    for word in x.split():
        if (word == 'but'):
            flag = 1
        if (word in dic):
            dic[word] = dic[word] + 1 if flag == 0 else dic[word] + 1
        else:
            dic[word] = 1 if flag == 0 else 1
    # END_YOUR_CODE
    return dic

# x = 'the a  the not animation master , is always welcome .'
# result = extractExtraCreditFeatures(x)
############################################################
# Problem 3: k-means
############################################################


def kmeans(examples, K, maxIters):
    '''
    examples: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters
    maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (around 35 lines of code expected)
    def distance(x1, x2):
        result = 0
        for f, v in x2.items():
            result += (x1.get(f, 0) - v) ** 2
        return result

    def average(points):
        n = float(len(points))
        result = {}
        for p in points:
            increment(result, 1 / n, p)
        return result

    centroids = random.sample(examples, K)
    old_assignments = []
    for _ in range(maxIters):
        center_points_pair = []
        assignments = []
        totalCost = 0
# ## map phase:
        for p in examples:
            dis = [distance(c, p) for c in centroids]
            newCenter = dis.index(min(dis))
            assignments.append(newCenter)
            totalCost += min(dis)
#           print dis, newCenter
            center_points_pair.append((newCenter, p))
        if assignments == old_assignments:
            break
        else:
            old_assignments = list(assignments)
        center_points_pair = sorted(center_points_pair, key=lambda item: item[0])
# ## reduce phase with groupby() and average():
        new_centroids = []
        for key, kpList in itertools.groupby(center_points_pair, key=lambda item:item[0]):
            pList = [ kp[1] for kp in kpList]
            new_centroids.append(average(pList))

#       print 'new centroids are', new_centroids
        centroids = new_centroids
#   print centroids, assignments, totalCost
    return centroids, assignments, totalCost





