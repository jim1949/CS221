#!/usr/bin/env python
"""
Grader for template assignment
Optionally run as grader.py [basic|all] to run a subset of tests
"""


import random, sys

from engine.const import Const
import graderUtil
import util
import collections
import copy
grader = graderUtil.Grader()
submission = grader.load('submission')


############################################################
# Manual problems

# .addBasicPart is a basic test and always run.
grader.addBasicPart('writeupValid', lambda : grader.requireIsValidPdf('writeup.pdf'), 0)




############################################################
# Problem 2: Emission Probability (7 points)

def test2a():
    ei = submission.ExactInference(10, 10)
    ei.skipElapse = True  # ## ONLY FOR PROBLEM 2
    ei.observe(55, 193, 200)
    grader.requireIsEqual(0.030841805296, ei.belief.getProb(0, 0))
    grader.requireIsEqual(0.00073380582967, ei.belief.getProb(2, 4))
    grader.requireIsEqual(0.0269846478431, ei.belief.getProb(4, 7))
    grader.requireIsEqual(0.0129150762582, ei.belief.getProb(5, 9))

    ei.observe(80, 250, 150)
    grader.requireIsEqual(0.00000261584106271, ei.belief.getProb(0, 0))
    grader.requireIsEqual(0.000924335357194, ei.belief.getProb(2, 4))
    grader.requireIsEqual(0.0295673460685, ei.belief.getProb(4, 7))
    grader.requireIsEqual(0.000102360275238, ei.belief.getProb(5, 9))

grader.addBasicPart('2a-0', test2a, 2, description="2a basic test for emission probabilities")


############################################################
# Problem 3: Transition Probability (7 points)

def test3a():
    ei = submission.ExactInference(30, 13)
    ei.elapseTime()
    grader.requireIsEqual(0.0105778989624, ei.belief.getProb(16, 6))
    grader.requireIsEqual(0.00250560512469, ei.belief.getProb(18, 7))
    grader.requireIsEqual(0.0165024135157, ei.belief.getProb(21, 7))
    grader.requireIsEqual(0.0178755550388, ei.belief.getProb(8, 4))

    ei.elapseTime()
    grader.requireIsEqual(0.0138327373012, ei.belief.getProb(16, 6))
    grader.requireIsEqual(0.00257237608713, ei.belief.getProb(18, 7))
    grader.requireIsEqual(0.0232612833688, ei.belief.getProb(21, 7))
    grader.requireIsEqual(0.0176501876956, ei.belief.getProb(8, 4))

grader.addBasicPart('3a-0', test3a, 2, description="3a basic test for transition probabilities")


############################################################
# Problem 4: Particle Filter (18 points)

def test4a_0():
    random.seed(3)

    pf = submission.ParticleFilter(30, 13)

    pf.observe(555, 193, 800)

    grader.requireIsEqual(0.015, pf.belief.getProb(20, 4))
    grader.requireIsEqual(0.135, pf.belief.getProb(21, 5))
    grader.requireIsEqual(0.85, pf.belief.getProb(22, 6))
    grader.requireIsEqual(0.0, pf.belief.getProb(8, 4))

    pf.observe(525, 193, 830)

    grader.requireIsEqual(0.0, pf.belief.getProb(20, 4))
    grader.requireIsEqual(0.01, pf.belief.getProb(21, 5))
    grader.requireIsEqual(0.99, pf.belief.getProb(22, 6))
    grader.requireIsEqual(0.0, pf.belief.getProb(8, 4))


grader.addBasicPart('4a-0', test4a_0, 2, description="4a basic test for PF observe")

def test4a_1():
    random.seed(3)
    pf = submission.ParticleFilter(30, 13)
    grader.requireIsEqual(69, len(pf.particles))  # This should not fail unless your code changed the random initialization code.

    pf.elapseTime()
    grader.requireIsEqual(200, sum(pf.particles.values()))  # Do not lose particles
    grader.requireIsEqual(66, len(pf.particles))  # Most particles lie on the same (row, col) locations

    grader.requireIsEqual(9, pf.particles[(3, 9)])
    grader.requireIsEqual(0, pf.particles[(2, 10)])
    grader.requireIsEqual(7, pf.particles[(8, 4)])
    grader.requireIsEqual(6, pf.particles[(12, 6)])
    grader.requireIsEqual(1, pf.particles[(7, 8)])
    grader.requireIsEqual(1, pf.particles[(11, 6)])
    grader.requireIsEqual(0, pf.particles[(18, 7)])
    grader.requireIsEqual(1, pf.particles[(20, 5)])

    pf.elapseTime()
    grader.requireIsEqual(200, sum(pf.particles.values()))  # Do not lose particles
    grader.requireIsEqual(61, len(pf.particles))  # Slightly more particles lie on the same (row, col) locations

    grader.requireIsEqual(6, pf.particles[(3, 9)])
    grader.requireIsEqual(0, pf.particles[(2, 10)])  # 0 --> 0
    grader.requireIsEqual(2, pf.particles[(8, 4)])
    grader.requireIsEqual(5, pf.particles[(12, 6)])
    grader.requireIsEqual(2, pf.particles[(7, 8)])
    grader.requireIsEqual(1, pf.particles[(11, 6)])
    grader.requireIsEqual(1, pf.particles[(18, 7)])  # 0 --> 1
    grader.requireIsEqual(0, pf.particles[(20, 5)])  # 1 --> 0

grader.addBasicPart('4a-1', test4a_1, 2, description="4a basic test for PF elapseTime")

def test4a_2():
    random.seed(3)
    pf = submission.ParticleFilter(30, 13)
    grader.requireIsEqual(69, len(pf.particles))  # This should not fail unless your code changed the random initialization code.

    pf.elapseTime()
    grader.requireIsEqual(66, len(pf.particles))  # Most particles lie on the same (row, col) locations
    pf.observe(555, 193, 800)

    grader.requireIsEqual(200, sum(pf.particles.values()))  # Do not lose particles
    grader.requireIsEqual(3, len(pf.particles))  # Most particles lie on the same (row, col) locations
    grader.requireIsEqual(0.025, pf.belief.getProb(20, 4))
    grader.requireIsEqual(0.035, pf.belief.getProb(21, 5))
    grader.requireIsEqual(0.0, pf.belief.getProb(21, 6))
    grader.requireIsEqual(0.94, pf.belief.getProb(22, 6))
    grader.requireIsEqual(0.0, pf.belief.getProb(22, 7))

    pf.elapseTime()
    grader.requireIsEqual(5, len(pf.particles))  # Most particles lie on the same (row, col) locations

    pf.observe(660, 193, 50)
    grader.requireIsEqual(0.0, pf.belief.getProb(20, 4))
    grader.requireIsEqual(0.0, pf.belief.getProb(21, 5))
    grader.requireIsEqual(0.095, pf.belief.getProb(21, 6))
    grader.requireIsEqual(0.0, pf.belief.getProb(22, 6))
    grader.requireIsEqual(0.905, pf.belief.getProb(22, 7))

grader.addBasicPart('4a-2', test4a_2, 3, description="4a basic test for PF observe AND elapseTime")




grader.grade()
