import os
import sys
# for deep copy
import copy
# for sleep and time measuring
import time

class GameEnum:
	GAME_UNDECIDED		= -1
	GAME_DRAW			= 0

	BOARD_UNFILLED		= 0

	PLAYER_HUMAN		= 1
	PLAYER_COMPUTER		= 2

	MAX_INT				= sys.maxunicode
	MIN_INT				= -sys.maxunicode - 1
	
# global variables are evil
# says everyone ever, until they need one
expandedStates = 0 # performance measurement, total states expanded

def utility(board):
	winner = GetGameWinner(board)
	if winner == GameEnum.GAME_DRAW:
		return 0
	elif winner == GameEnum.PLAYER_COMPUTER:
		return 100
	else:
		return -100
		
def terminalTest(board):
	return GetGameWinner(board) != -1

def sucessors(state, player):
	stateList = []
	for idx in range(9):
		if state[idx] == GameEnum.BOARD_UNFILLED:
			newState = copy.deepcopy(state)
			newState[idx] = player
			newState[9] = idx; # store the play move after the regular board array, in the 9th position
			stateList.append(newState)

	return stateList

def GetSideUtility(state):
	utility = 0
	linesToCheck = [
		# horizontal
		[0, 1, 2],
		[3, 4, 5],
		[6, 7, 8],
		# vertical
		[0, 3, 6],
		[1, 4, 7],
		[2, 5, 8],
		# diagonals
		[0, 4, 8],
		[2, 4, 6]
	]
	
	for line in linesToCheck:
		x = GameEnum.BOARD_UNFILLED
		for idx in line:
			if state[idx] != GameEnum.BOARD_UNFILLED: # check if someone already made a move on the line
				if x != GameEnum.BOARD_UNFILLED and x != state[idx]: # did both players make a move on the line? ignore it if yes
					x = GameEnum.BOARD_UNFILLED
					break

				x = state[idx]

		if x == GameEnum.PLAYER_HUMAN:
			utility -= 1
		elif x == GameEnum.PLAYER_COMPUTER:
			utility += 1
		# else it's a line for both players, so no utility change

	return utility

def GetBoardSymbolForSlot(board, idx):
	if board[idx] == GameEnum.BOARD_UNFILLED:
		return str(idx + 1)
	elif board[idx] == GameEnum.PLAYER_HUMAN:
		return 'X'
	elif board[idx] == GameEnum.PLAYER_COMPUTER:
		return 'O'
		
	assert False

def pcMove(board, algorithm):
	if algorithm == 1:
		return MiniMax.Decision(board)
	if algorithm == 2:
		return AlphaBeta.Search(board)	
	
# does sanity checking on the board
def DoMove(board, player, idx):

	assert board[idx] == GameEnum.BOARD_UNFILLED
	
	board[idx] = player
	drawBoard(board)

# allows the choice of algorithm for computer
def computerAlgorithm():
	algorithm = None
	print ('Computer algorithm')
	print ('1. MiniMax')
	print ('2. Alpha-Beta')
	while algorithm not in [1,2]:
		algorithm = int(input('Choose algorithm: '))
	return algorithm

def drawBoard(board):
	print('\nTic Tac Toe')
	print('\n   |   |')
	print(' ' + GetBoardSymbolForSlot(board, 0) + ' | ' + GetBoardSymbolForSlot(board, 1) + ' | ' + GetBoardSymbolForSlot(board, 2))
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + GetBoardSymbolForSlot(board, 3) + ' | ' + GetBoardSymbolForSlot(board, 4) + ' | ' + GetBoardSymbolForSlot(board, 5))
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + GetBoardSymbolForSlot(board, 6) + ' | ' + GetBoardSymbolForSlot(board, 7) + ' | ' + GetBoardSymbolForSlot(board, 8))
	print('   |   |\n')

def GetGameWinner(state):
	linesToCheck = [
		# horizontal
		[0, 1, 2],
		[3, 4, 5],
		[6, 7, 8],
		# vertical
		[0, 3, 6],
		[1, 4, 7],
		[2, 5, 8],
		# diagonals
		[0, 4, 8],
		[2, 4, 6]
	]

	for line in linesToCheck:
		x = GameEnum.BOARD_UNFILLED
		for idx in line:
			if state[idx] == GameEnum.BOARD_UNFILLED:
				x = GameEnum.BOARD_UNFILLED
				break

			if x != GameEnum.BOARD_UNFILLED and x != state[idx]: # did both players make a move on the line? ignore it if yes
				x = GameEnum.BOARD_UNFILLED
				break

			x = state[idx]

		if x != GameEnum.BOARD_UNFILLED:
			return x

	for idx in range(0, 9):
		if state[idx] == GameEnum.BOARD_UNFILLED:
			return GameEnum.GAME_UNDECIDED
			
	return GameEnum.GAME_DRAW

# asks the player for a move
def DoPlayerMove(board):
	# board displays as [1, 2, ..., 9], which is not the way the array is stored, so we need to subtract 1
	position = int(input('Choose a number: ')) - 1
	DoMove(board, GameEnum.PLAYER_HUMAN, position)

	winner = GetGameWinner(board)
	return winner;

def DoAIMove(board, algorithm):
	startTime = time.clock()
	
	global expandedStates
	expandedStates = 0
	
	position = pcMove(board, algorithm)
	DoMove(board, GameEnum.PLAYER_COMPUTER, position)
	endTime = time.clock()
	# print out elapsed time for performance measurement
	print ("Calc time: %s seconds" % (endTime - startTime))
	print ("Expanded states: %s" % expandedStates)

	winner = GetGameWinner(board)
	return winner

def PlayGame():
	# initial board - [0, 0, 0, 0, 0, 0, 0, 0, 0]
	# 9th position used for 'play done', used for states
	board = [GameEnum.BOARD_UNFILLED] * 10
	algorithm = computerAlgorithm()
	drawBoard(board)
	
	# allows the choice of who plays first
	s = int(input('Who goes first?\nType 1 for Player or 2 for Computer: '))
	if (s == 2):
		print ("This might take a moment")
		DoAIMove(board, algorithm)
	
	while True:
		winner = DoPlayerMove(board)
		if winner != GameEnum.GAME_UNDECIDED:
			return winner

		winner = DoAIMove(board, algorithm)
		if winner != GameEnum.GAME_UNDECIDED:
			return winner

######################################
# AlfaBeta algorithm
class AlphaBeta:
	@staticmethod
	def Search(state):
		value, playMove = AlphaBeta.MaxValue_Init(state, GameEnum.MIN_INT, GameEnum.MAX_INT)
		return playMove
		
	@staticmethod
	def MaxValue_Init(state, alfa, beta):
		assert terminalTest(state) == False
		
		global expandedStates
		expandedStates += 1
		
		playMove = -1
		value = GameEnum.MIN_INT
		for s in sucessors(state, GameEnum.PLAYER_COMPUTER):
			minVal = AlphaBeta.MinValue(s, alfa, beta)
			
			# apply secondary utility 'heuristic', serves to distinguish between 'all options are shit' states
			minVal += GetSideUtility(s)
			
			if minVal >= value:
				value = minVal
				playMove = s[9] # play move is stored on the position after the array

			if value >= beta:
				return (value, playMove)

			alfa = max(alfa, value)
			
		assert playMove != -1
		return (value, playMove)
		
	@staticmethod
	def MaxValue(state, alfa, beta):
		global expandedStates
		expandedStates += 1
		
		if terminalTest(state):
			return utility(state)
			
		value = GameEnum.MIN_INT
		for s in sucessors(state, GameEnum.PLAYER_COMPUTER):
			value = max(value, AlphaBeta.MinValue(s, alfa, beta))

			if value >= beta:
				return value

			alfa = max(alfa, value)
			
		return value

	@staticmethod
	def MinValue(state, alfa, beta):
		global expandedStates
		expandedStates += 1
		
		if terminalTest(state):
			return utility(state)
			
		value = GameEnum.MAX_INT
		for s in sucessors(state, GameEnum.PLAYER_HUMAN):
			value = min(value, AlphaBeta.MaxValue(s, alfa, beta))

			if value <= alfa:
				return value

			beta = min(beta, value)
			
		return value

#######################################
# MiniMax algorithm
class MiniMax:
	@staticmethod
	def Decision(state):
		value, playMove = MiniMax.maxValue_Init(state)
		return playMove
		
	@staticmethod
	def maxValue_Init(state):
		assert terminalTest(state) == False
		
		global expandedStates
		expandedStates += 1
		
		playMove = -1
		value = GameEnum.MIN_INT
		for s in sucessors(state, GameEnum.PLAYER_COMPUTER):
			minVal = MiniMax.minValue(s)
			
			minVal += GetSideUtility(s)
			
			if minVal >= value:
				value = minVal
				playMove = s[9]
		
		assert playMove != -1
		return(value,playMove)
		
		
	@staticmethod
	def maxValue(state):
		global expandedStates
		expandedStates += 1
		
		if terminalTest(state):
			return utility(state)
			
		value = GameEnum.MIN_INT
		for s in sucessors(state, GameEnum.PLAYER_COMPUTER):
			value = max(value, MiniMax.minValue(s))
		return value
		
	@staticmethod
	def minValue(state):
		global expandedStates
		expandedStates += 1
		
		if terminalTest(state):
			return utility(state)
		
		value = GameEnum.MAX_INT
		for s in sucessors(state, GameEnum.PLAYER_HUMAN):
			value = min(value, MiniMax.maxValue(s))
		return value

def main():
	winner = PlayGame()
	
	assert winner != GameEnum.GAME_UNDECIDED

	if winner == GameEnum.GAME_DRAW:
		print ('Draw')
	elif winner == GameEnum.PLAYER_HUMAN:
		print ('Player won')
	elif winner == GameEnum.PLAYER_COMPUTER:
		print ('Computer won')

if __name__ == "__main__":
	main()


