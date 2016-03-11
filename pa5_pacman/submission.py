from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    
    The GameState class is defined in pacman.py and you might want to look into that for 
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
    self.index = 0  # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      pacman won, pacman lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
	
      gameState.isWin():
        Returns True if it's a winning state
	
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue
    """

    # BEGIN_YOUR_CODE (around 30 lines of code expected)
    # self is MultiAgentSearchAgent, which has:
    #    index
    #    evaluationFunction
    #    depth

    def isEnd(gameState):
        return gameState.getLegalActions(self.index) == []

    # returns the (minimax value, action)
    def recurse(gameState, index, d):
        if isEnd(gameState) or d == 0:
            return (self.evaluationFunction(gameState), None)

        # is pacMan
        elif index == 0:
            VA = (float('-inf'), None)
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                VA = max(VA, (recurse(newGameState, index + 1, d)[0], action))
            return VA
        # is oppenent:
        else:  # is  opponent
            VA = (float('inf'), None)
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    VA = min(VA, (recurse(newGameState, 0, d - 1)[0], action))
                else:
                    VA = min(VA, (recurse(newGameState, index + 1, d)[0], action))
            return VA

    (V, A) = recurse(gameState, self.index, self.depth)
#     print "value is", V
    return A
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (around 50 lines of code expected)
    def isEnd(gameState):
        return gameState.getLegalActions(self.index) == []

    # returns the (minimax value, action)
    def recurse(gameState, index, d, alpha, beta):
        if isEnd(gameState) or d == 0:
            return (self.evaluationFunction(gameState), None)

        # is pacMan
        elif index == 0:
            VA = (float('-inf'), None)
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                VA = max(VA, (recurse(newGameState, index + 1, d, alpha, beta)[0], action))
                # only below two lines are newly added, decide when to prune and maintain alpha
                if VA[0] > beta: return VA  # here it's saying: this node found a large alpha as VA[0], if not supressed it'll choose this.
                # However, above tree already supressed everything larger than beta, so prune this node from further examining the rest children
                alpha = max(alpha, VA[0])
            return VA
        # is oppenent:
        else:  # is  opponent
            VA = (float('inf'), None)
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    VA = min(VA, (recurse(newGameState, 0, d - 1, alpha, beta)[0], action))
                else:
                    VA = min(VA, (recurse(newGameState, index + 1, d, alpha, beta)[0], action))
                if alpha > VA[0]: return VA  # here it's saying: this node found a strong supression point at VA[0], 'claiming' everything above it will not exist
                # However, above tree already found an alpha larger than this beta, so prune this node from further examining the rest children
                beta = min(beta, VA[0])
            return VA

    alpha = float('-inf')
    beta = float('inf')
    (V, A) = recurse(gameState, self.index, self.depth, alpha, beta)
#     print "value is", V
    return A

    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (around 25 lines of code expected)

    def isEnd(gameState):
        return gameState.getLegalActions(self.index) == []

    # returns the (minimax value, action)
    def recurse(gameState, index, d):
        # base case:
        if isEnd(gameState) or d == 0:
            return (self.evaluationFunction(gameState), None)
        # is pacMan:
        elif index == 0:
            VA = (float('-inf'), None)
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                VA = max(VA, (recurse(newGameState, index + 1, d)[0], action))
            return VA
        # is oppenent:
        else:  # is  opponent
            VA = (0.0, None)
            prob = 1.0 / len(gameState.getLegalActions(index))
            for action in gameState.getLegalActions(index):
                if action == Directions.STOP: continue
                newGameState = gameState.generateSuccessor(index, action)
                if index == gameState.getNumAgents() - 1:
                    VA = (VA[0] + prob * (recurse(newGameState, 0, d - 1)[0]), action)
                else:
                    VA = (VA[0] + prob * (recurse(newGameState, index + 1, d)[0]), action)
            return VA

    (V, A) = recurse(gameState, self.index, self.depth)
    return A
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (around 30 lines of code expected)
  newPos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  ghostPos = currentGameState.getGhostPositions()
  scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

  finalScore = currentGameState.getScore()
  food = currentGameState.getFood()

  if newPos[0] > 7 and newPos[0] < 12 and newPos[1] == 5:
      finalScore -= 20
  for i in range(20):
    for j in range(5):
      if(food[i][j]) == True:
        manhattenDis = abs(i - newPos[0]) + abs(j - newPos[1])
        if manhattenDis == 1:
            finalScore += 30
        if manhattenDis == 2:
            finalScore += 2
        else:
            finalScore += 3.0 / manhattenDis


  minGhost = float('inf')
  for i in range(len(ghostPos)):
    x, y = ghostPos[i]
    ghostDis = (abs(x - newPos[0]) + abs(y - newPos[1]))
    if ghostDis < minGhost: minGhost = ghostDis
    if ghostDis == 0:
      finalScore -= 500
    else:
      finalScore -= 200 / (ghostDis - 0.5)


  capsule = currentGameState.getCapsules()
  for i in range(len(capsule)):
    x, y = capsule[i]
    manhattenDis = abs(x - newPos[0]) + abs(y - newPos[1])
    if minGhost == 1:
        if manhattenDis == 1 :
            finalScore += 5;
        else:
            finalScore += 1.0 / manhattenDis



  return finalScore

  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction


