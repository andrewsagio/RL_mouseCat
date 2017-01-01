# my Q-learning exercise
import random
import numpy as np
class QLearn:
    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9, mode='logistic'):

        self.q = {} # the action-reward lookup table. key is (state, action) tuple. value is the expected reward Q
        self.mode = mode # learning mode
        self.epsilon = epsilon  # possibility of taking a random action
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for reward learned
        self.actions = actions # all available actions (int)


    def learn(self, lastState, lastAction, reward, state):
        oldValue = self.q.get( (lastState, lastAction), None )
        if oldValue is None:
            newValue = reward
        else:
            Q = {a:self.q.get((state, a), 0) for a in self.actions}  # expected reward for all actions of CURRENT state
            maxQ = max(Q.values())  # maximum expected reward for current state
            newValue = oldValue + self.alpha * ( reward + self.gamma*maxQ - oldValue)
        self.q[(lastState, lastAction)] = newValue # update q table
        return

    def chooseAction(self, state):
        if self.mode == 'random':
            # random exploration at fixed probability epsilon
            if random.random() < self.epsilon:
                # random action for exploration
                return random.sample(self.actions,1)[0]
            # select action that has best expected return
            Q = {a: self.q.get((state, a), 0) for a in self.actions} # expected reward for all actions
            maxQ = max(Q.values())  # maximum expected reward
            bestActions = [i for i in Q if Q[i] ==maxQ] # find best actions (can be more than one)
            best  = random.sample(bestActions, 1)[0]  # choose an random action if tie
            return best
        elif self.mode == 'logistic':
            T = 1.
            Qv = np.array([self.q.get((state, a), 1e-5) for a in self.actions])  # default to 0 is problematic with normalization
            prob = np.exp(Qv/T)
            prob = np.cumsum(prob/ sum(prob) )
            return self.actions[np.where(prob >= random.random())[0][0]]










