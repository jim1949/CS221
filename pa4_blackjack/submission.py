import collections, util, math, random

############################################################

############################################################
# Problem 2a

class ValueIteration(util.MDPAlgorithm):

    # Implement value iteration.  First, compute V_opt using the methods
    # discussed in class.  Once you have computed V_opt, compute the optimal
    # policy pi.  Note that ValueIteration is an instance of util.MDPAlgrotithm,
    # which means you will need to set pi and V (see util.py).
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        self.V = {}
        self.pi = {}
        for state in mdp.states:
            self.V[state] = 0
        newV = {}
        while (1):  # O(SAS')
            for state in mdp.states:  # O(S)
                maxV = float("-infinity")
                for action in mdp.actions(state):  # O(A)
                    value = 0
#                     if not mdp.succAndProbReward(state, action):  # reached end state
#                         continue;
                    for newState, prob, reward in mdp.succAndProbReward(state, action):  # O(S')
                        value += prob * (reward + mdp.discount() * self.V[newState])
                    if value > maxV:
                        maxV = value
                        self.pi[state] = action
                if maxV == float("-infinity"):
                    maxV = 0
                newV[state] = maxV

            converged = True
            for state in mdp.states:
                if newV[state] - self.V[state] > epsilon:
                    converged = False
            if converged == True: break
            self.V = dict(newV)  # don't point to the same V object!

#         print self.pi

        # END_YOUR_CODE



############################################################
# Problem 2b

# If you decide 2b is true, prove it in writeup.pdf and put "return None" for
# the code blocks below.  If you decide that 2b is false, construct a
# counterexample by filling out this class and returning an alpha value in
# counterexampleAlpha().
class CounterexampleMDP(util.MDP):
    def __init__(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return
        # END_YOUR_CODE

    def startState(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return 0
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        if state == 1:
            return set()
        if state == 0:
            return set(['stay', 'quit'])
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        if state == 1:
            return list()
        if state == 0:
            if action == 'stay':
                return [(0, 1. / 3., 4), (1, 2. / 3., 4)]
            if action == 'quit':
                return [(1, 1, 5)]
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (around 5 lines of code expected)
        return 1
        # END_YOUR_CODE

def counterexampleAlpha():
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return 1. / 3.
    # END_YOUR_CODE


# mdp = CounterexampleMDP()
# algo = ValueIteration()
# algo.solve(mdp)

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.  The second element is the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.  The final element
    # is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None
    # The second element of the state is the index of the peeked card, not the actual value of the peeked card, which is self.cardValues[nextCardIdx]
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (around 55 lines of code expected)
        total, nextCardIdx, multiplicityVec = state
        candidates = []
        if multiplicityVec == None:
            return []
        #############################################################
        if action == 'Take':
            if nextCardIdx != None:  # previously peeked
                total += self.cardValues[nextCardIdx]
                prob = 1
                reward = 0
                if total > self.threshold:
                    newState = (total, None, None)
                else:
                    newMultiplicityVec = list(multiplicityVec)
                    newMultiplicityVec[nextCardIdx] -= 1
                    if sum(newMultiplicityVec) <= 0:
                        reward = total
                        newState = (total, None, None)
                    else:
                        newState = (total, None, tuple(newMultiplicityVec))
                candidates.append((newState, prob, reward))
            else:  # previously didn't peek
                totalPossibles = sum(multiplicityVec)
                for i in xrange(len(self.cardValues)):
                    newMultiplicityVec = list(multiplicityVec)
                    prob = newMultiplicityVec[i] / float(totalPossibles)
                    if prob == 0: continue
                    reward = 0

                    newTotal = total
                    newTotal += self.cardValues[i]
                    if newTotal > self.threshold:
                        newState = (newTotal, None, None)
                    else:
                        assert (newMultiplicityVec[i] > 0)
                        newMultiplicityVec[i] -= 1
                        if sum(newMultiplicityVec) <= 0:
                            reward = newTotal
                            newState = (newTotal, None, None)
                        else:
                            newState = (newTotal, None, tuple(newMultiplicityVec))
                    candidates.append((newState, prob, reward))
        #############################################################
        if action == 'Peek':
            if nextCardIdx != None:  # can't peek twice
                return []
            else:
                totalPossibles = sum(multiplicityVec)
                for i in xrange(len(self.cardValues)):
                    newMultiplicityVec = list(multiplicityVec)
                    prob = newMultiplicityVec[i] / float(totalPossibles)
                    if prob == 0: continue

                    reward = -self.peekCost
                    newState = (total, i, multiplicityVec)
                    candidates.append((newState, prob, reward))
        #############################################################
        if action == 'Quit':
            newState = (total, None, None)
            prob = 1
            reward = total
            candidates.append((newState, prob, reward))

        return candidates
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (around 5 lines of code expected)
    return BlackjackMDP([6, 4, 16], 15, 20, 1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = collections.Counter()
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (around 15 lines of code expected)
        if newState == None: return
        newAction = max((self.getQ(state, action), action) for action in self.actions(state))[1]
        residual = self.getQ(state, action) - (float(reward) + self.discount * self.getQ(newState, newAction))
        for f, v in self.featureExtractor(state, action):
            self.weights[f] -= self.getStepSize() * residual * v
        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning



############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).  Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (around 10 lines of code expected)
    features = []
    key1 = (total, action)
    features.append((key1, 1))

    if (counts != None) and (sum(counts) != 0):
        key2 = ['Presense']
        for i in counts:
            if i == 0:
                key2.append(1)
            else:
                key2.append(0)
        key2.append(action)
        features.append((tuple(key2), 1))

        for i in range(len(counts)):
            cardType = 'Number_' + str(i + 1)
            key3 = (cardType, counts[i], action)
            features.append((key3, 1))

    return features
    # END_YOUR_CODE

############################################################
# Problem 4d: changing mdp


