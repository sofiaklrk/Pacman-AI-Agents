#multiAgents.py (original)
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        considers food, ghost locations.
        food heuristic:
        prefer states with:
        1.food closer to Pacman
        2.fewer remaining food pellets
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return -float("inf")

        score = successorGameState.getScore()

        # Food
        if newFood: #distance to the closest food
            foodDistances = [manhattanDistance(newPos, food) for food in newFood]
            score += 10.0 / (min(foodDistances) + 1e-5)

        # Ghosts
        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())
            if ghost.scaredTimer > 0: #if ghost is scared, reward approaching it
                score += 200.0 / (dist + 1e-5) if dist > 0 else 200.0
            else: #if ghost is active, heavily panelize close proximity
                if dist < 2:
                    score -= 500
                else:
                    score -= 2.0 / (dist + 1e-5)

        # Penalize stopping
        from game import Directions
        if action == Directions.STOP:
            score -= 10

        return float(score)


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def minimax(state, agentIndex, depth):
            # Terminal state
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            # Pacman (MAX)
            if agentIndex == 0:
                value = -float("inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, minimax(successor, 1, depth))
                return value

            # Ghosts (MIN)
            else:
                value = float("inf")
                nextAgent = agentIndex + 1

                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)

                    if nextAgent == numAgents:
                        # Last ghost → next ply
                        value = min(value, minimax(successor, 0, depth - 1))
                    else:
                        value = min(value, minimax(successor, nextAgent, depth))

                return value

        # Root call: select best action for Pacman
        bestValue = -float("inf")
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = minimax(successor, 1, self.depth)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphabeta(state, agentIndex, depth, a, b):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            # Pacman (MAX)
            if agentIndex == 0:
                value = -float("inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, alphabeta(successor, 1, depth, a, b))

                    if value > b: # prune
                        return value
                    a = max(a, value)

                return value

            # Ghosts (MIN)
            else:
                value = float("inf")
                nextAgent = agentIndex + 1

                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)

                    if nextAgent == numAgents:
                        value = min(value, alphabeta(successor, 0, depth - 1, a, b))
                    else:
                        value = min(value, alphabeta(successor, nextAgent, depth, a, b))

                    if value < a: # prune
                        return value
                    b = min(b, value)

                return value

        bestValue = -float("inf")
        bestAction = None
        a = -float("inf")
        b = float("inf")

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = alphabeta(successor, 1, self.depth, a, b)

            if value > bestValue:
                bestValue = value
                bestAction = action

            if bestValue > b:
                return bestAction
            a = max(a, bestValue)

        return bestAction
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()

            # Pacman (MAX)
            if agentIndex == 0:
                value = -float("inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, expectimax(successor, 1, depth))
                return value

            # Ghosts (CHANCE)
            else:
                values = []
                nextAgent = agentIndex + 1

                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)

                    if nextAgent == numAgents:
                        values.append(expectimax(successor, 0, depth - 1))
                    else:
                        values.append(expectimax(successor, nextAgent, depth))


                return sum(values) / float(len(values)) # Expected value (uniform probability)

        bestValue = -float("inf")
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value = expectimax(successor, 1, self.depth)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Terminal states
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")

    score = currentGameState.getScore()

    pacmanPos = currentGameState.getPacmanPosition()
    newfood = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    #Food:
    if newfood:
        foodDistances = [manhattanDistance(pacmanPos, food) for food in newfood]
        score += 10.0 / min(foodDistances)
        score -= 4 * len(newfood)

    #Ghosts:
    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        dist = manhattanDistance(pacmanPos, ghostPos)

        if ghost.scaredTimer > 0:
            if dist > 0:
                score += 20.0 / dist
        else:
            if dist < 2:
                score -= 1000
            elif dist > 0:
                score -= 2.0 / dist

    return score
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


  