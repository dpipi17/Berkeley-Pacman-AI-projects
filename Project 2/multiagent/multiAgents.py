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
import sys

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
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # my evaluation Function finds distance to the nearest food
        # if this distance is small, evaluation function returns larger value
        # and action which goes to the state with smallest distance to food will be chosen


        # initialize min distance to the food as MAX_INT
        minDistanceToFood = sys.maxsize

        # get food location list for the current state
        foodList = currentGameState.getFood().asList()

        # for every food location update min distance
        for food in foodList:
          minDistanceToFood = min(minDistanceToFood, manhattanDistance(newPos, food))

        # check for every ghost 
        for ghostState in newGhostStates:
          ghostPos = ghostState.getPosition()

          # if after this action distance between pacman and ghost is less or equal than one
          # this is terrible action and because that evaluation function returns INT_MIN
          if manhattanDistance(ghostPos, newPos) <= 1:
            return -1 * sys.maxsize

        # because less distance is better, we have to multiply our answer by -1
        return -1 * minDistanceToFood

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

        # check if this state is game end state, it has no childs in tree
        def isLeaf(depth, state):
          return state.isWin() or state.isLose()

        # recursive function which retunrs result if both (pacman and ghosts) play optimal
        def Minimax(state, depth, agentIndex):
          
          # base case, where we stop to move down in the tree
          if depth == self.depth or isLeaf(depth, state):
            return self.evaluationFunction(state)

          # its ghost's turn
          if agentIndex != 0:
            
            # if next is pacmans turn we have to increase depth in the tree
            if (agentIndex + 1) % state.getNumAgents() == 0:
              depth += 1

            # create list where we store every result for each action
            minim = []

            # for every legal action
            for action in state.getLegalActions(agentIndex):
              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # add to the list value, which is returned by recursive function
              minim.append(Minimax(nextState, depth, (agentIndex + 1) % state.getNumAgents()))

            # return minimum from the list, because ghost always chooses minimum value from its childs
            return min(minim)


          # its pacman's turn
          else:

            # create list where we store every result for each action
            maxim = []

            # for every legal action
            for action in state.getLegalActions(agentIndex):
              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # add to the list value, which is returned by recursive function
              maxim.append(Minimax(nextState, depth, 1))

            # return maximum from the list, because pacman always chooses maximum value from its childs
            return max(maxim)
        

        # initialize result action and current maximum
        resAction = ''
        maxim = 0

        # for every legal action for pacman
        for action in gameState.getLegalActions(self.index):
          # get state, where you go with that action
          nextState = gameState.generateSuccessor(self.index, action)

          # if that state is winning state for pacman, he/she should do that action
          # and return this action as a result
          if nextState.isWin():
            return action

          # call recursive function
          currValue = Minimax(nextState, 0, self.index + 1)

          # check if there is larger value, if is, update currmax and result action
          if currValue > maxim or resAction == '':
            maxim = currValue
            resAction = action
  
        # return optimal result for pacman
        return resAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # check if this state is game end state, if is, it has no childs in tree
        def isLeaf(depth, state):
          return state.isWin() or state.isLose()

        # recursive function which retunrs result if both (pacman and ghosts) play optimal
        # with optimization
        def AlphaBeta(state, depth, agentIndex, currMaxim, currMinim):
        
          # base case, where we stop to move down in the tree
          if depth == self.depth or isLeaf(depth, state):
            return self.evaluationFunction(state)


          # its ghost's turn
          if agentIndex != 0:
            
            # if next is pacmans turn we have to increase depth in the tree
            if (agentIndex + 1) % state.getNumAgents() == 0:
              depth += 1

            # initialize minim as a INT_MAX
            minim = sys.maxsize

            # for every legal action
            for action in state.getLegalActions(agentIndex):

              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # update minim 
              minim = min(minim, AlphaBeta(nextState, depth, (agentIndex + 1) % state.getNumAgents(), currMaxim, currMinim))

              # if current value is less than currMaxim, there is no need to continue algorithm and check other childs of this node
              # because ghost never chooses node, which value is larger than minim
              # and pacman already has child whicb value is larger than minim.(currMaxim node is that node)
              if minim < currMaxim:
                return minim
              currMinim = min(currMinim, minim)

            return minim

          # its pacman's turn
          else:

            # initialize maxim as a INT_MIN
            maxim = -1 * sys.maxsize - 1

            # for every legal action
            for action in state.getLegalActions(agentIndex):

              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # update maxim
              maxim = max(maxim, AlphaBeta(nextState, depth, 1, currMaxim, currMinim))

              # if current maxim is larger then currMinim, there is no need to continue algoritm and check other childs of this node
              # pacman never chooses node, which value is less than current maxim.
              # and ghost already has a node which value is less than current maxim.(currMinim node is that node)
              if maxim > currMinim:
                return maxim
              currMaxim = max(currMaxim, maxim)

            return maxim
        


        # initialize result action and maximum
        resAction = ''
        maxim = 0

        # initialize current maxim and current minim
        currMaxim = -1 * sys.maxsize - 1
        currMinim = sys.maxsize

        # for every legal action for pacman
        for action in gameState.getLegalActions(self.index):
           # get state, where you go with that action
          nextState = gameState.generateSuccessor(self.index, action)

          # call recursive function
          currValue = AlphaBeta(nextState, 0, self.index + 1, currMaxim, currMinim)

          # update currMaxim
          currMaxim = max(currMaxim, currValue)

          # check if there is larger value, than update maxim and result action
          if currValue > maxim or resAction == '':
            maxim = currValue
            resAction = action
  
        return resAction




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

        # check if this state is game end state, it has no childs in tree
        def isLeaf(depth, state):
          return state.isWin() or state.isLose()

        # recursive function
        def Expectimax(state, depth, agentIndex):
        
          # base case, where we stop to move down in the tree
          if depth == self.depth or isLeaf(depth, state):
            return self.evaluationFunction(state)

          # its ghost's turn
          if agentIndex != 0:
            
            # if next is pacmans turn we have to increase depth in the tree
            if (agentIndex + 1) % state.getNumAgents() == 0:
              depth += 1

            # create list where we store every result for each action
            values = []

            # for every legal action
            for action in state.getLegalActions(agentIndex):

              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # add to the list value, which is returned by recursive function
              values.append(Expectimax(nextState, depth, (agentIndex + 1) % state.getNumAgents()))

            # in expectimax ghost chooses every node for equal probability
            # because that we choose arithmetic mean of values
            sumOfResults = float(sum(values))
            avg = sumOfResults / len(state.getLegalActions(agentIndex))
            return avg


          # its pacman's turn
          else:

            # create list where we store every result for each action
            maxim = []

            # for every legal action
            for action in state.getLegalActions(agentIndex):
              # get state, where you go with that action
              nextState = state.generateSuccessor(agentIndex, action)

              # add to the list value, which is returned by recursive function
              maxim.append(Expectimax(nextState, depth, 1))

            # return maximum from the list, because pacman always chooses maximum value from its childs
            return max(maxim)
        

        # initialize result action and current maximum
        resAction = ''
        maxim = 0
         
        # for every legal action for pacman
        for action in gameState.getLegalActions(self.index):

          # get state, where you go with that action
          nextState = gameState.generateSuccessor(self.index, action)

          # if that state is winning state for pacman, he/she should do that action
          # and return this action as a result
          if nextState.isWin():
            return action

          # call recursive function
          currValue = Expectimax(nextState, 0, self.index + 1)

          # check if there is larger value, if is, update currmax and result action
          if currValue > maxim or resAction == '':
            maxim = currValue
            resAction = action
  
        return resAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

      i used 4 function for this evaluation function.
      first function is distance to nearest food in this state.
      second function is sum of the distances to the each ghost.
      third function shows if the ghost is scared.
      4th function gives score in this state.

      evaluation function returns combination of this 4 function. 
    """
    "*** YOUR CODE HERE ***"

    ghostStates = currentGameState.getGhostStates()
    pos = currentGameState.getPacmanPosition()


    "*** YOUR CODE HERE ***"

    # check, if this state is winning state for pacman, eval function should return infinity(INT_Max in this situation)
    if currentGameState.isWin():
      return sys.maxsize
  
    # check, if this state is winning state for ghosts, eval function should retun minus infinity (INT_MIN  in this situation)
    if currentGameState.isLose():
      return -1 * sys.maxsize - 1

    # initialize min distance to the food
    minDistanceToFood = sys.maxsize

    # get food locations list for the current state
    foodList = currentGameState.getFood().asList()

    # for every food location
    for food in foodList:

      # update min distance to the food
      minDistanceToFood = min(minDistanceToFood, manhattanDistance(pos, food))
    
    # initialize ghostDist, which will be sum of every distance from pacman to eacg ghost
    ghostDist = 0

    # initialize ghostDanger, this is parameter, which shows if ghost is scared
    ghostDanger = 1

    # for every ghost
    for ghost in ghostStates:
      ghostPos = ghost.getPosition()

      # add current distance to ghostDist
      ghostDist += manhattanDistance(ghostPos, pos)

      # if in this state, distance from pacman to the ghost is less or equal than 1
      # this state is not good, and eval func should return minus infinity (INT_MIN in this situation)
      if manhattanDistance(ghostPos, pos) <= 1:
        return -1 * sys.maxsize

      # check if ghost is scared and update ghostDanger parameter
      if ghost.scaredTimer != 0:
       ghostDanger = 100
    
    # return combination of four function
    return currentGameState.getScore() + 1 / float(minDistanceToFood) - 1 / float(ghostDist) - 1 / float(ghostDanger)

# Abbreviation
better = betterEvaluationFunction

