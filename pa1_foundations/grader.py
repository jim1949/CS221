#!/usr/bin/env python

import graderUtil, collections, random

grader = graderUtil.Grader()
submission = grader.load('submission')

############################################################
# Problems 1 and 2

grader.addBasicPart('writeupValid', lambda : grader.requireIsValidPdf('writeup.pdf'))


############################################################
# Problem 3a: computeMaxWordLength

grader.addBasicPart('3a-0', lambda :
        grader.requireIsEqual('longest', submission.computeMaxWordLength('which is the longest word')))


############################################################
# Problem 3b: createExistsFunction

def test():
    func = submission.createExistsFunction('the quick brown fox jumps over the lazy fox')
    grader.requireIsEqual(True, func('lazy'))
    grader.requireIsEqual(False, func('laz'))
grader.addBasicPart('3b-0', test)


############################################################
# Problem 3c: manhattanDistance

grader.addBasicPart('3c-0', lambda : grader.requireIsEqual(6, submission.manhattanDistance((3, 5), (1, 9))))


############################################################
# Problem 3d: dotProduct

grader.addBasicPart('3d-0', lambda : grader.requireIsEqual(15, submission.sparseVectorDotProduct(collections.Counter({'a': 5}), collections.Counter({'b': 2, 'a': 3}))))


############################################################
# Problem 3e: incrementSparseVector

def test():
    v = collections.Counter({'a': 5})
    submission.incrementSparseVector(v, 2, collections.Counter({'b': 2, 'a': 3}))
    grader.requireIsEqual(collections.Counter({'a': 11, 'b': 4}), v)
grader.addBasicPart('3e-0', test)


############################################################
# Problem 3f

def test3f():
    grader.requireIsEqual((set(['the', 'fox']), 2), submission.computeMostFrequentWord('the quick brown fox jumps over the lazy fox'))
grader.addBasicPart('3f-0', test3f)


############################################################
# Problem 3g

def test3g():
    # Test around bases cases
    grader.requireIsEqual(0, submission.computeLongestPalindrome(""))
    grader.requireIsEqual(1, submission.computeLongestPalindrome("a"))
    grader.requireIsEqual(2, submission.computeLongestPalindrome("aa"))
    grader.requireIsEqual(submission.computeLongestPalindrome("ab"), 1)
    grader.requireIsEqual(submission.computeLongestPalindrome("animal"), 3)
grader.addBasicPart('3g-0', test3g)


grader.grade()
