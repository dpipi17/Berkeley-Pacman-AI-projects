# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        states = mdp.getStates()

        # temporary dictionary
        tempValue = dict()

        # repeat moves for iterations time
        for _ in range(self.iterations):

            # calculate Value for each state
            for state in states:
               
                # if state is terminal, its value is always 0
                if self.mdp.isTerminal(state):
                    tempValue[state] = 0
                else: 

                    # if state is not terminal
                    # calculate every qvalue for this state
                    # and value for this state will be max(qvalues)
                    possibleActions = mdp.getPossibleActions(state)
                    qValues = []
                    for action in possibleActions:
                        qValues.append(self.computeQValueFromValues(state, action))
                    

                    # choose maximum from calculated qValues to get Value
                    # V*(state) = max(for each action) Q*(state, action)
                    tempValue[state] = max(qValues)
                    
            # write data from temporary dictionary to real value dictionary
            for state in states:
                self.values[state] = tempValue[state]




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # get mdp model
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        
        # This code is same as formula:
        # Q*(s, a) = Sum(s') (T(s, a, s') * (R(s, a, s') + gama * V*(s')))
        # in code s is state, a is action, s' is nextState, T - prob, R-rewart , gama - discount, V*(s') - self.getValue(nextState)
        qvalue = 0
        for nextState, prob in statesAndProbs:
            qvalue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))

        return qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        # this code is for formula : pi*(state) = argmax(action) Q*(state, action)
        # for every action from this state, choose that action which gives maximal Qvalue
        # we only need to calculate qvalues, from Value, which is already calculated
        possibleActions = self.mdp.getPossibleActions(state)
        resultAction = None
        currMaxQValue = 0
        
        # for every Action
        for action in possibleActions:
            # calculate qValue for this action,from this state, from Value
            currQValue = self.computeQValueFromValues(state, action)

            # if this qValue is maximum so far, update action and currMaxQvalue
            if currQValue > currMaxQValue or resultAction == None:
                currMaxQValue = currQValue
                resultAction = action
        
        # if state is terminal, resultAction will be None
        return resultAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
