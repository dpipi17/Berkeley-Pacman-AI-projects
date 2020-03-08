# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    # after answerNoise is zero, Values will be change
    # if pacman goes to the low-reward state, he get 0.9 * 1 = 0.9 points
    # if he goes to the high-reward state, he gets 0.9^5 * 10 = 5.9049 points
    # thats why he crosses the bridge
    answerDiscount = 0.9
    answerNoise = 0
    return answerDiscount, answerNoise

def question3a():
    # because answeNoise is 0, pacman is risking the cliff
    # because livingReward is too low, pacman prefers close exist to get more point
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = -5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    # because noise is 0.1 and not 0, pacman is avoiding the clif
    # because discount is too low, pacman prefers close exist
    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    # because Noise is 0, pacman is risking the cliff
    # because discount is 1 and pacman prefers distant exit
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = -0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    # because noise is 0.1 and not 0, pacman is avoiding the clif
    # because discount is 1 and pacman prefers distant exit to get more points
    answerDiscount = 1
    answerNoise = 0.1
    answerLivingReward = -0.01
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    # because noise is 0, and discount is 1 and livingreward is 100(positive number)
    # pacman prefers to never end the game, because he gets more points when moves
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 100
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    # If not possible, return 'NOT POSSIBLE'
    return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
