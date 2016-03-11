import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return 0
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return state == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        # return action, nextState, cost
        choices = []
        for i in range(state + 1, len(self.query) + 1):
            choices.append((i - state, i, self.unigramCost(self.query[state:i])))

        return choices
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    state = 0;
    words = []
    for i in ucs.actions:
        word = query[state:state + i]
        state = state + i
        words.append(word)
    return ' '.join(words)
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        th, preWord = state
        return th == len(self.queryWords)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 10 lines of code expected)
        # return action, nextState, cost
        choices = []
        th, preWord = state
        nextWordPiece = self.queryWords[th]
        nextWords = self.possibleFills(nextWordPiece)
        if len(nextWords) == 0:
            nextWords = set([nextWordPiece])
        for nextWord in nextWords:
            cost = self.bigramCost(preWord, nextWord)
            choices.append((nextWord, (th + 1, nextWord), cost))
        return choices
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)

    result = []
    for word in ucs.actions:
        result.append(word)
    return ' '.join(result)

    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return (0, wordsegUtil.SENTENCE_BEGIN)
        # END_YOUR_CODE

    def isGoal(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        th, word = state
        return th == len(self.query)
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        th, preWord = state
        choices = []
        for i in range(th + 1, len(self.query) + 1):
            nextWordPiece = self.query[th:i]
            nextWords = self.possibleFills(nextWordPiece)
            for nextWord in nextWords:
                cost = self.bigramCost(preWord, nextWord)
                choices.append((nextWord, (i, nextWord), cost))

        return choices
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    problem = JointSegmentationInsertionProblem(query, bigramCost, possibleFills)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(problem)
    result = []
    for word in ucs.actions:
        result.append(word)
    return ' '.join(result)
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
