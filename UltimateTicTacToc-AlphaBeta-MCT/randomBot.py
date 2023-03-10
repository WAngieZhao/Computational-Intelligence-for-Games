'''
Random player class definition
'''

import random

class RandomBot():
	
	def __init__(self, symbol):
		
		self.symbol = symbol

	def getMove(self, board, prevMove):

		nextMoves, nextSymbol = board.getValidMoves(prevMove)
		
		return random.choice(nextMoves)