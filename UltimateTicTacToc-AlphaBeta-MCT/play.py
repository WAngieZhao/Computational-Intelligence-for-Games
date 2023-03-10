'''
Reference:
Game board reference from: 
	Author:@vaibhav.garg (year). 
	Date: 4th Aug'20
	Retrieved from: https://github.com/VAIBHAV-2303/MonteCarloTreeSearch 
'''
# File running the main game loop

# from colorama import Fore, Style
from bigBoard import BigBoard
from mcts import MCTS
from copy import *
from randomBot import RandomBot
from alpha_beta import AlphaBeta
import sys

if __name__ == "__main__":

	run_number = 100		# The number of rounds to run
	if len(sys.argv) > 1:
		run_number = int(sys.argv[1])
	print("Number of rounds to run:", run_number)

	p1_win, p2_win, draw_count = 0, 0, 0
	# print("Please input number of rounds to run")
	# run_number = int(input())

	# Choose first player
	print("Please decide player1")
	print("1. MCTS\n2. AlphaBeta\n3. Random")
	choice = input()
	# choice = '1' # player 1 choice
	print("choice 1 is", choice)
	if choice == '1':
		p1 = MCTS('X', compTime=0.01)
	elif choice == '2':
		p1 = AlphaBeta('X')
	elif choice == '3':
		p1 = RandomBot('X')
	else:
		raise Exception("Should input value from 1 to 3")

	# Choose second player
	print("Please decide player2")
	# print("1. MCTS\n2. AlphaBeta\n3. Random")
	choice = input()
	# choice = '2' # player 2 choice
	print("choice 2 is", choice)
	if choice == '1':
		p2 = MCTS('O', compTime=0.01)
	elif choice == '2':
		p2 = AlphaBeta('O')
	elif choice == '3':
		p2 = RandomBot('O')
	else:
		raise Exception("Should input value from 1 to 3")

	for i in range(run_number):
		print("round", i + 1, ":", end="")
		# Initializing game board
		board = BigBoard()

		# Game loop
		# board.print()
		prevMove = None
		while True:

			# P1 turn
			move = None
			validMoves = board.getValidMoves(prevMove)[0]
			while move not in validMoves:
				# print("It is P1's turn now.")
				move = p1.getMove(deepcopy(board), prevMove)
			
			board.playMove(move, 'X')
			# print("Move played by p1:", move)
			prevMove = move
			# board.print()
			curState = board.getState()
			if curState[0] == 'W':
				print("P1 won!")
				p1_win += 1
				break
			elif curState[0] == 'D':
				print("Draw!")
				draw_count += 1
				break

			# P2 turn
			move = None
			validMoves = board.getValidMoves(prevMove)[0]
			while move not in validMoves:
				# print("It is P2's turn now.")
				move = p2.getMove(deepcopy(board), prevMove) 
				
			board.playMove(move, 'O')
			# print("Move played by p2:", move)
			prevMove = move
			# board.print()
			curState = board.getState()
			if curState[0] == 'W':
				print("P2 won!")
				p2_win += 1
				break
			elif curState[0] == 'D':
				print("Draw!")
				draw_count += 1
				break
		
	print("p1_win:", p1_win)
	print("p2_win:", p2_win)
	print("draw_count:", draw_count)
	print("p1/total", p1_win / run_number)