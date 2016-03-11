import graderUtil

grader = graderUtil.Grader()
submission = grader.load('submission')

FINAL_GRADE = True
SEED = 'testing' # random seed at the beginning of each question for more fairness in grading...                              
BIG_NEGATIVE = -10000

from game import Agent
from ghostAgents import RandomGhost, DirectionalGhost
import random, math, traceback, sys, os

import pacman, time, layout, textDisplay
textDisplay.SLEEP_TIME = 0
textDisplay.DRAW_EVERY = 1000
thismodule = sys.modules[__name__]


grader.addBasicPart('writeupValid', lambda : grader.requireIsValidPdf('writeup.pdf'))


def run(layname, pac, ghosts, nGames = 1, name = 'games'):
  """
  Runs a few games and outputs their statistics.
  """
  starttime = time.time()
  lay = layout.getLayout(layname,3)
  disp = textDisplay.NullGraphics()

  print '*** Running %s on' % name, layname,'%d time(s).' % nGames
  games = pacman.runGames(lay, pac, ghosts, disp, nGames, False, catchExceptions=True )
  print '*** Finished running %s on' % name, layname,'after %d seconds.' % (time.time() - starttime)
  
  stats = {'time': time.time() - starttime, 'wins': [g.state.isWin() for g in games].count(True), 'games': games, 'scores': [g.state.getScore() for g in games], 'timeouts': [g.agentTimeout for g in games].count(True)}
  print '*** Won %d out of %d games. Average score: %f ***' % (stats['wins'], len(games), sum(stats['scores']) * 1.0 / len(games))

  return stats



def test0(agentName):
  stats = {}
  if agentName == 'alphabeta':
    stats = run('smallClassic', submission.AlphaBetaAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s(depth %d)' % ('alphabeta', 2))
  elif agentName == 'minimax':
    stats = run('smallClassic', submission.MinimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s(depth %d)' % ('minimax', 2))
  else:
    stats = run('smallClassic', submission.ExpectimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)], name='%s(depth %d)' % ('expectimax', 2))
  if stats['timeouts'] > 0:
    grader.fail('Your '+agentName+' agent timed out on smallClassic.  No autograder feedback will be provided.')
    return
  grader.assignFullCredit()



grader.addBasicPart('1b-0', lambda : test0('minimax'), 4, description='Tests minimax for timeout on smallClassic.')
grader.addBasicPart('2-0', lambda : test0('alphabeta'), 4, description='Tests alphabeta for timeout on smallClassic.')
grader.addBasicPart('3b-0', lambda : test0('expectimax'), 4, description='Tests expectimax for timeout on smallClassic.')


grader.grade()
