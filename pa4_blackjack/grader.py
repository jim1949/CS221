#!/usr/bin/env python
import random, util, collections

import graderUtil
grader = graderUtil.Grader()
submission = grader.load('submission')


############################################################
# Manual problems

grader.addBasicPart('writeupValid', lambda :
      grader.requireIsValidPdf('writeup.pdf'), 0)

grader.addManualPart('1a', 3)

def testIteration(algorithm):
    mdp = util.NumberLineMDP()
    goldPi = collections.defaultdict(lambda: 1)
    goldV = {}
    values = [l.split() for l in open('2a.gold')]
    for state, value in values:
        goldV[int(state)] = float(value)
    algorithm.solve(mdp, .0001)
    for state in range(-5, 6):
        if not grader.requireIsEqual(goldPi[state], algorithm.pi[state]):
            print '   action for state: {}'.format(state)
        if not grader.requireIsLessThan(.001, abs(goldV[state] - algorithm.V[state])):
            print '   value for state: {}'.format(state)


def test2a():
    testIteration(submission.ValueIteration())
grader.addBasicPart('2a', test2a, 3, description="Basic test for ValueIteration using NumberLineMDP.")


def test3a():
    mdp1 = submission.BlackjackMDP(cardValues=[1, 5], multiplicity=2,
                                   threshold=10, peekCost=1)
    startState = mdp1.startState()
    preBustState = (6, None, (1, 1))
    postBustState = (11, None, None)

    mdp2 = submission.BlackjackMDP(cardValues=[1, 5], multiplicity=2,
                                   threshold=15, peekCost=1)
    preEmptyState = (11, None, (1, 0))

    tests = [([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)],
          mdp1, startState, 'Take'),
         ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)],
          mdp1, startState, 'Peek'),
         ([((0, None, None), 1, 0)], mdp1, startState, 'Quit'),
         ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)],
          mdp1, preBustState, 'Take'),
         ([], mdp1, postBustState, 'Take'),
         ([], mdp1, postBustState, 'Peek'),
         ([], mdp1, postBustState, 'Quit'),
         ([((12, None, None), 1, 12)], mdp2, preEmptyState, 'Take')]
    for gold, mdp, state, action in tests:
        if not grader.requireIsEqual(gold,
                                     mdp.succAndProbReward(state, action)):
            print '   state: {}, action: {}'.format(state, action)
grader.addBasicPart('3a', test3a, 4, description="Basic test for succAndProbReward() that covers several edge cases.")


def test3b():
    mdp = submission.peekingMDP()
    vi = submission.ValueIteration()
    vi.solve(mdp)
    grader.requireIsEqual(mdp.threshold, 20)
    grader.requireIsEqual(mdp.peekCost, 1)
    f = len([a for a in vi.pi.values() if a == 'Peek']) / float(len(vi.pi.values()))
    grader.requireIsGreaterThan(.1, f)
grader.addBasicPart('3b', test3b, 2, description="Test for peekingMDP().  Ensure that in at least 10% of states, the optimal policy is to peek.")


def test4a():
    mdp = util.NumberLineMDP()
    mdp.computeStates()
    rl = submission.QLearningAlgorithm(mdp.actions, mdp.discount(),
                                       submission.identityFeatureExtractor,
                                       0)
    # We call this here so that the stepSize will be 1
    rl.numIters = 1

    rl.incorporateFeedback(0, 1, 0, 1)
    grader.requireIsEqual(0, rl.getQ(0, -1))
    grader.requireIsEqual(0, rl.getQ(0, 1))

    rl.incorporateFeedback(1, 1, 1, 2)
    grader.requireIsEqual(0, rl.getQ(0, -1))
    grader.requireIsEqual(0, rl.getQ(0, 1))
    grader.requireIsEqual(0, rl.getQ(1, -1))
    grader.requireIsEqual(1, rl.getQ(1, 1))

    rl.incorporateFeedback(2, -1, 1, 1)
    grader.requireIsEqual(1.9, rl.getQ(2, -1))
    grader.requireIsEqual(0, rl.getQ(2, 1))

grader.addBasicPart('4a', test4a, 3, maxSeconds=10, description="Basic test for incorporateFeedback() using NumberLineMDP.")


grader.addManualPart('4b', 3)

def test4c():
    mdp = submission.BlackjackMDP(cardValues=[1, 5], multiplicity=2,
                                  threshold=10, peekCost=1)
    mdp.computeStates()
    rl = submission.QLearningAlgorithm(mdp.actions, mdp.discount(),
                                       submission.blackjackFeatureExtractor,
                                       0)
    # We call this here so that the stepSize will be 1
    rl.numIters = 1

    rl.incorporateFeedback((7, None, (0, 1)), 'Quit', 7, (7, None, None))
    grader.requireIsEqual(28, rl.getQ((7, None, (0, 1)), 'Quit'))
    grader.requireIsEqual(7, rl.getQ((7, None, (1, 0)), 'Quit'))
    grader.requireIsEqual(14, rl.getQ((2, None, (0, 2)), 'Quit'))
    grader.requireIsEqual(0, rl.getQ((2, None, (0, 2)), 'Take'))
grader.addBasicPart('4c', test4c, 3, maxSeconds=10, description="Basic test for blackjackFeatureExtractor.  Runs QLearningAlgorithm using blackjackFeatureExtractor, then checks to see that Q-values are correct.")

grader.addManualPart('4d', 2)

grader.grade()
