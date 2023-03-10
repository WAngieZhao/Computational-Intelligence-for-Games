"The Monte Carlo Tree Search (MCTS) algorithm was implemented"

import random
import math
import time
from copy import *
import math

class MCTSNode:
    def __init__(self, state, prevMove, parent=None):
        self.state = state
        self.prevMove = prevMove
        self.parent = parent
        self.children = []
        self.num_visits = 0
        self.total_reward = 0
    
    def add_child(self, prevMove, child_state):
        child = MCTSNode(child_state, prevMove, self)
        self.children.append(child)
        return child
    
    def update(self, reward):
        self.num_visits += 1
        self.total_reward += reward
    
    def UCB1(self, exploration_constant):
        if self.num_visits == 0:
            return float('inf')
        return (self.total_reward / self.num_visits) + exploration_constant * math.sqrt(math.log(self.parent.num_visits) / self.num_visits)

class MCTS:
    def __init__(self, symbol, compTime=0.01):
        self.symbol = symbol
        self.C = math.sqrt(2)
        self.compTime = compTime

    def getMove(self, board, prevMove):
        # Creting a root node
        root = MCTSNode(deepcopy(board),prevMove)
        startTime = time.time()
        while time.time() - startTime < self.compTime:
             self.mcts_search(root, prevMove)
        return self.choose(root)

    def mcts_search(self, root, prevMove):
         # Selection
        node = root
        curState = node.state.getState()
        # while not fully_expanded()
        while curState[0] == 'N':
            best_child = None
            max_UCB1 = float('-inf')
            for child in node.children:
                UCB1 = child.UCB1(self.C)
                if UCB1 > max_UCB1:
                    max_UCB1 = UCB1
                    best_child = child
            if best_child is not None:
                node = best_child
            else:
                break

         # Expansion
        # if not node.fully_expanded:
        if curState[0] == 'N':
            # P2
            # Play move with next move
            nextMoves, nextSymbol = node.state.getValidMoves(node.prevMove)
            new_state = node.state
            
            #print(len(node.children))
            #print(nextMoves)
            move = nextMoves[len(node.children)]
            new_state.playMove(move,nextSymbol)
            node = node.add_child(move, new_state)
        
        # Simulation
        reward = self.simulate(node.state, prevMove)
        
        # Backpropagation
        while node is not None:
            node.update(reward)
            node = node.parent

    def choose(self, root):
        # Return the best move
        best_move = None
        max_reward = float('-inf')
        for child in root.children:
            if child.total_reward > max_reward:
                max_reward = child.total_reward
                best_move = child.prevMove
        return best_move

    def simulate(self, board, prevMove):
        curState = board.getState()
        if curState[0] == 'N':
            nextMoves, nextSymbol = board.getValidMoves(prevMove)
			# Randmoly choose the next move
            nextRandom = random.choice(nextMoves)
            board.playMove(nextRandom, nextSymbol)
            return self.simulate(board, nextRandom)
        else: # if curState[0] != 'N', the game terminate
            if curState[0] == 'W':
                if curState[1] == self.symbol:
                    return 1 # Win
                else:
                    return -1 # Loss
            else:
                return 0 # Draw

