import datetime
from collections import defaultdict
import math
import random

# Takes the allowed CPU time in seconds and
# returns a function that takes a position and returns the move suggested 
def mcts_policy(cpu_time):
    def returned_function(state):
        tree = MCTS()
        begin = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - begin) < datetime.timedelta(seconds=cpu_time):
            tree.rollout(state)
        return tree.choose(state)
    return returned_function


class MCTS:
    """
    self.r = total payoff of each state, not averaged
    self.N = total time of visit for each state
    self.children_move = a dictionary of possible move of each state
        - key = state
        - value = list of possible emove
    self.unexplored_states = a dictionary of unexplored state move of each state
        - key = state
        - value = list of unexplored state
    """
    def __init__(self):
        self.rN = defaultdict(lambda: [0,0])
        self.children_move = dict()
        self.unexplored_states = dict()

    def choose(self, state):
        # Choose a state randomly if it is unexplored/not expanded
        if state not in self.children_move:
            return random.choice(state.get_actions())

        def payoff(child):
            child_state = state.successor(child)
            N = self.rN[child_state][1]
            if N == 0:
                return float("-inf")
            return N

        return max(self.children_move[state], key=payoff)

    # Steps of MCTS: traverse tree -> expand -> simultae -> update/backpropagate
    def rollout(self, state):
        path = self.traverse(state)
        node = path[-1]
        self.expand(node)
        payoff = self.simulate(node)
        self.update(path, payoff)

    # Travrse the tree and select next node to expande
    def traverse(self, state):
        path = []
        while True:
            path.append(state)
            # The state is unexplored/not expanded
            if state not in self.children_move or state.is_terminal():
                return path

            #unexplored_states = self.unexplored_states[state]
            if self.unexplored_states[state]:
                n = self.unexplored_states[state].pop()
                path.append(n)
                return path

            # All states at current level is explored, selecting with uct/ucb
            state = state.successor(self.uct(state))

    # Expand the node by getting all possible actions from current state
    def expand(self, state):
        # The state is already expanded
        if state in self.children_move:
            return  
        self.children_move[state] = state.get_actions()

        states_after_move = []
        for move in self.children_move[state]:
            states_after_move.append(state.successor(move))
        self.unexplored_states[state] = states_after_move
    
    # Play to terminal position
    def simulate(self, state):
        while not state.is_terminal():
            state = state.successor(random.choice(state.get_actions()))
        return state.payoff()

    # Update/Backpropagate the payoff value and visit count
    def update(self, path, payoff):
        for state in reversed(path):
            self.rN[state][0] += payoff
            self.rN[state][1] += 1

    # Using UCB to select the node to traverse
    # optimize speed
    def uct(self, state):
        #assert all(n in self.children for n in self.children[node])
        log_N = math.log(self.rN[state][1])
        def ucb(n):
            n = state.successor(n)
            rN = self.rN[n]
            if not state.actor():
                return (rN[0] / rN[1]) + 1.8 * math.sqrt(log_N / rN[1])
            else:
                return (-1) * (rN[0]/ rN[1]) + 1.8 * math.sqrt(log_N / rN[1])

        return max(self.children_move[state], key=ucb)
    