#!/usr/bin/env python

from logic import *

import pickle, gzip, os, random
import graderUtil

grader = graderUtil.Grader()
submission = grader.load('submission')

# name: name of this formula (used to load the models)
# predForm: the formula predicted in the submission
# preconditionForm: only consider models such that preconditionForm is true
def checkFormula(name, predForm, preconditionForm=None):
    filename = os.path.join('models', name + '.pklz')
    objects, targetModels = pickle.load(gzip.open(filename))
    # If preconditionion exists, change the formula to
    preconditionPredForm = And(preconditionForm, predForm) if preconditionForm else predForm
    predModels = performModelChecking([preconditionPredForm], findAll=True, objects=objects)
    ok = True
    def hashkey(model): return tuple(sorted(str(atom) for atom in model))
    targetModelSet = set(hashkey(model) for model in targetModels)
    predModelSet = set(hashkey(model) for model in predModels)
    for model in targetModels:
        if hashkey(model) not in predModelSet:
            grader.fail("Your formula (%s) says the following model is FALSE, but it should be TRUE:" % predForm)
            ok = False
            printModel(model)
            return
    for model in predModels:
        if hashkey(model) not in targetModelSet:
            grader.fail("Your formula (%s) says the following model is TRUE, but it should be FALSE:" % predForm)
            ok = False
            printModel(model)
            return
    grader.addMessage('You matched the %d models' % len(targetModels))
    grader.addMessage('Example model: %s' % rstr(random.choice(targetModels)))
    grader.assignFullCredit()

# name: name of this formula set (used to load the models)
# predForms: formulas predicted in the submission
# predQuery: query formula predicted in the submission
def addParts(name, numForms, predictionFunc):
    # part is either an individual formula (0:numForms), all (combine everything)
    def check(part):
        predForms, predQuery = predictionFunc()
        if len(predForms) < numForms:
            grader.fail("Wanted %d formulas, but got %d formulas:" % (numForms, len(predForms)))
            for form in predForms: print '-', form
            return
        if part == 'all':
            checkFormula(name + '-all', AndList(predForms))
        elif part == 'run':
            # Actually run it on a knowledge base
            # kb = createResolutionKB()  # Too slow!
            kb = createModelCheckingKB()

            # Need to tell the KB about the objects to do model checking
            filename = os.path.join('models', name + '-all.pklz')
            objects, targetModels = pickle.load(gzip.open(filename))
            for obj in objects:
                kb.tell(Atom('Object', obj))

            # Add the formulas
            for predForm in predForms:
                response = kb.tell(predForm)
                showKBResponse(response)
                grader.requireIsEqual(CONTINGENT, response.status)
            response = kb.ask(predQuery)
            showKBResponse(response)

        else:  # Check the part-th formula
            checkFormula(name + '-' + str(part), predForms[part])

    def createCheck(part): return lambda : check(part)  # To create closure

    for part in range(numForms) + ['all', 'run']:
        if part == 'all':
            description = 'test implementation of %s for %s' % (part, name)
        elif part == 'run':
            description = 'test implementation of %s for %s' % (part, name)
        else:
            description = 'test implementation of statement %s for %s' % (part, name)
        grader.addBasicPart(name + '-' + str(part), createCheck(part), maxPoints=1, maxSeconds=10000, description=description)

############################################################
# Problem 1: propositional logic

grader.addBasicPart('formula1a', lambda : checkFormula('formula1a', submission.formula1a()), 1, description='Test formula 1a implementation')
grader.addBasicPart('formula1b', lambda : checkFormula('formula1b', submission.formula1b()), 1, description='Test formula 1b implementation')
grader.addBasicPart('formula1c', lambda : checkFormula('formula1c', submission.formula1c()), 1, description='Test formula 1c implementation')

############################################################
# Problem 2: first-order logic

formula2a_precondition = AntiReflexive('Mother')
formula2b_precondition = AntiReflexive('Child')
formula2c_precondition = AntiReflexive('Child')
formula2d_precondition = AntiReflexive('Parent')
grader.addBasicPart('formula2a', lambda : checkFormula('formula2a', submission.formula2a(), formula2a_precondition), 1, description='Test formula 2a implementation')
grader.addBasicPart('formula2b', lambda : checkFormula('formula2b', submission.formula2b(), formula2b_precondition), 1, description='Test formula 2b implementation')
grader.addBasicPart('formula2c', lambda : checkFormula('formula2c', submission.formula2c(), formula2c_precondition), 1, description='Test formula 2c implementation')
grader.addBasicPart('formula2d', lambda : checkFormula('formula2d', submission.formula2d(), formula2d_precondition), 1, description='Test formula 2d implementation')

############################################################
# Problem 3: liar puzzle

# Add liar-[0-5], liar-all, liar-run
addParts('liar', 6, submission.liar)

############################################################
# Problem 4: Modus Ponens

grader.addManualPart('4-1', 5, description='Test CNF conversion and new Modus ponens rule to derive C')

grader.addManualPart('4-2', 5, description='Test usage of the resolution rule to derive D')

############################################################
# Problem 5: odd and even integers

# Add ints-[0-5], ints-all, ints-run
addParts('ints', 6, submission.ints)

grader.addManualPart('5-2', 5, description='Test argument that there is no finite model where all 7 formulas are consistent')

############################################################
# Problem 6: Natural language interface parsing

from nlparser import Utterance, parseUtterance

def testExtraCredit(sentence, targetDerivation):
    utterance = Utterance(sentence, processorClass=submission.createLanguageProcessor())
    print '>>>', utterance
    derivations = parseUtterance(utterance, submission.createNLIGrammar(), verbose=3)
    if not derivations:
        raise Exception('Error: Parsing failed. (0 derivations)')
    grader.requireIsEqual(targetDerivation, derivations[0].form)


def test_6_1():
    sentence = 'Every hound is a dog.'
    target = ('tell', Forall('$x', Implies(Atom('Hound', '$x'), Atom('Dog', '$x'))))
    testExtraCredit(sentence, target)

def test_6_2():
    sentence = 'Pluto is a hound.'
    target = ('tell', Atom('Hound', 'pluto'))
    testExtraCredit(sentence, target)

def test_6_3():
    sentence = 'Is Pluto a dog?'
    target = ('ask', Atom('Dog', 'pluto'))
    testExtraCredit(sentence, target)

def getParsedFormula(sentence):
    utterance = Utterance(sentence, processorClass=submission.createLanguageProcessor())
    print '>>>', utterance
    derivations = parseUtterance(utterance, submission.createNLIGrammar(), verbose=3)
    if not derivations:
        raise Exception('Error: Parsing failed. (0 derivations)')
    return derivations[0].form[1]

def test_6_ec3():
    sentence = 'If a dog has a foot, then it has a leg.'

    kb = createResolutionKB()

    # construct a true statement
    myDog = Constant('tom')
    kb.tell(Atom('Dog', myDog))
    foot1 = Constant('somefootzzz')
    kb.tell(Atom('Foot', foot1))
    kb.tell(Atom('Has', myDog, foot1))

    kb.tell(getParsedFormula(sentence))

    trueStatement = Exists('$x', And(Atom('Leg', '$x'), Atom('Has', myDog, '$x')))
    uncertainStatement = Exists('$x', And(Atom('Tail', '$x'), Atom('Has', myDog, '$x')))
    falseStatement = Not(Exists('$x', And(Atom('Leg', '$x'), Atom('Has', myDog, '$x'))))

    grader.requireIsEqual("Yes.", str(kb.ask(trueStatement)))
    grader.requireIsEqual("I don't know.", str(kb.ask(uncertainStatement)))
    grader.requireIsEqual("No.", str(kb.ask(falseStatement)))





grader.addHiddenPart('6-1', test_6_1, 0, description='Test natural language rule number 1', extraCredit=True)
grader.addHiddenPart('6-2', test_6_2, 0, description='Test natural language rule number 2', extraCredit=True)
grader.addHiddenPart('6-3', test_6_3, 0, description='Test natural language rule number 3', extraCredit=True)

grader.addHiddenPart('6-ec3', test_6_ec3, 1, maxSeconds=10000, description='Test natural language rule number 6 semantics', extraCredit=True)
grader.grade()
