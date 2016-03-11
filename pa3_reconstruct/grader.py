#!/usr/bin/python

import graderUtil
import util
import sys
import wordsegUtil


CORPUS = 'leo-will.txt'

_realUnigramCost, _realBigramCost, _possibleFills = None, None, None

def getRealCosts():
    global _realUnigramCost, _realBigramCost, _possibleFills

    if _realUnigramCost is None:
        sys.stdout.write('Training language cost functions [corpus: %s]... ' % CORPUS)
        sys.stdout.flush()

        _realUnigramCost, _realBigramCost = wordsegUtil.makeLanguageModels(CORPUS)
        _possibleFills = wordsegUtil.makeInverseRemovalDictionary(CORPUS, 'aeiou')

        print 'Done!'
        print ''

    return _realUnigramCost, _realBigramCost, _possibleFills


def add_parts_1(grader, submission):

    def t_1b_1():
        def unigramCost(x):
            if x in ['and', 'two', 'three', 'word', 'words']:
                return 1.0
            else:
                return 1000.0

        grader.requireIsEqual('', submission.segmentWords('', unigramCost))
        grader.requireIsEqual('word', submission.segmentWords('word', unigramCost))
        grader.requireIsEqual('two words', submission.segmentWords('twowords', unigramCost))
        grader.requireIsEqual('and three words', submission.segmentWords('andthreewords', unigramCost))

    grader.addBasicPart('1b-1', t_1b_1, maxPoints=0, maxSeconds=2)

    def t_1b_2():
        unigramCost, _, _ = getRealCosts()
        grader.requireIsEqual('word', submission.segmentWords('word', unigramCost))
        grader.requireIsEqual('two words', submission.segmentWords('twowords', unigramCost))
        grader.requireIsEqual('and three words', submission.segmentWords('andthreewords', unigramCost))

    grader.addPart('1b-2', t_1b_2, maxPoints=1, maxSeconds=2)



def add_parts_2(grader, submission):

    def t_2b_1():
        def bigramCost(a, b):
            corpus = [wordsegUtil.SENTENCE_BEGIN] + 'beam me up scotty'.split()
            if (a, b) in list(zip(corpus, corpus[1:])):
                return 1.0
            else:
                return 1000.0

        def possibleFills(x):
            fills = {
                'bm'   : set(['beam', 'bam', 'boom']),
                'm'    : set(['me', 'ma']),
                'p'    : set(['up', 'oop', 'pa', 'epe']),
                'sctty': set(['scotty']),
            }
            return fills.get(x, set())

        grader.requireIsEqual(
            '',
            submission.insertVowels([], bigramCost, possibleFills)
        )
        grader.requireIsEqual( # No fills
            'zz$z$zz',
            submission.insertVowels(['zz$z$zz'], bigramCost, possibleFills)
        )
        grader.requireIsEqual(
            'beam',
            submission.insertVowels(['bm'], bigramCost, possibleFills)
        )
        grader.requireIsEqual(
            'me up',
            submission.insertVowels(['m', 'p'], bigramCost, possibleFills)
        )
        grader.requireIsEqual(
            'beam me up scotty',
            submission.insertVowels('bm m p sctty'.split(), bigramCost, possibleFills)
        )

    grader.addBasicPart('2b-1', t_2b_1, maxPoints=1, maxSeconds=2)



def add_parts_3(grader, submission):


    def t_3b_1():
        def bigramCost(a, b):
            if b in ['and', 'two', 'three', 'word', 'words']:
                return 1.0
            else:
                return 1000.0

        fills_ = {
            'nd': set(['and']),
            'tw': set(['two']),
            'thr': set(['three']),
            'wrd': set(['word']),
            'wrds': set(['words']),
        }
        fills = lambda x: fills_.get(x, set())

        grader.requireIsEqual('', submission.segmentAndInsert('', bigramCost, fills))
        grader.requireIsEqual('word', submission.segmentAndInsert('wrd', bigramCost, fills))
        grader.requireIsEqual('two words', submission.segmentAndInsert('twwrds', bigramCost, fills))
        grader.requireIsEqual('and three words', submission.segmentAndInsert('ndthrwrds', bigramCost, fills))

    grader.addBasicPart('3b-1', t_3b_1, maxPoints=1, maxSeconds=2)

    def t_3b_2():
        unigramCost, _, _ = getRealCosts()
        bigramCost = lambda a, b: unigramCost(b)

        fills_ = {
            'nd': set(['and']),
            'tw': set(['two']),
            'thr': set(['three']),
            'wrd': set(['word']),
            'wrds': set(['words']),
        }
        fills = lambda x: fills_.get(x, set())

        grader.requireIsEqual(
            'word',
            submission.segmentAndInsert('wrd', bigramCost, fills))
        grader.requireIsEqual(
            'two words',
            submission.segmentAndInsert('twwrds', bigramCost, fills))
        grader.requireIsEqual(
            'and three words',
            submission.segmentAndInsert('ndthrwrds', bigramCost, fills))

    grader.addPart('3b-2', t_3b_2, maxPoints=1, maxSeconds=2)



def grade():
    grader = graderUtil.Grader()
    submission = grader.load('submission')

    # Avoid timeouts during later non-basic parts.
    grader.addPart('init', lambda: getRealCosts(), maxPoints=0, maxSeconds=15)

    add_parts_1(grader, submission)
    add_parts_2(grader, submission)
    add_parts_3(grader, submission)

    grader.grade()




if __name__ == "__main__":
    grade()
