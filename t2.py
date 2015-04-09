import os
import sys
# for deep copy
import copy
# for sleep
import time

class GameEnum:
	GAME_UNDECIDED		= -1
	GAME_DRAW			= 0

	BOARD_UNFILLED		= 0

	PLAYER_HUMAN		= 1
	PLAYER_COMPUTER		= 2

	MAX_INT				= sys.maxint
	MIN_INT				= -sys.maxint - 1

#clear = lambda: os.system(['clear','cls'][os.name == 'nt'])

def GetBoardSymbolForSlot(board, idx):
	if board[idx] == GameEnum.BOARD_UNFILLED:
		return str(idx + 1)
	elif board[idx] == GameEnum.PLAYER_HUMAN:
		return 'X'
	elif board[idx] == GameEnum.PLAYER_COMPUTER:
		return 'O'
		
	assert False

def drawBoard(board):
	#clear()
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

def menu():
	first = None
	algorithm = None
	flag = True
	print "------------"
	print "Jogo do Galo"
	print "------------"


#	
#def computerAlgorithm(comp):
#	alg = None
#	print "Algoritmo"
#	print "1. MiniMax"
#	print "2. Alpha-Beta"
#	while alg not in [1,2]:
#		alg = int(raw_input("Escolha o algoritmo: "))
#	return alg

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

# does sanity checking on the board
def DoMove(board, player, idx):

	assert board[idx] == GameEnum.BOARD_UNFILLED
	
	board[idx] = player
	drawBoard(board)

def PlayGame():
	# initial board - [0, 0, 0, 0, 0, 0, 0, 0, 0]
	# 9th position used for 'play done', used for states
	board = [GameEnum.BOARD_UNFILLED] * 10

	drawBoard(board)
	
	while True:
		# person plays first
		# board displays as [1, 2, ..., 9], which is not the way the array is stored, so we need to subtract 1
		position = int(input("Choose a number: ")) - 1
		DoMove(board, GameEnum.PLAYER_HUMAN, position)

		winner = GetGameWinner(board)
		if winner != GameEnum.GAME_UNDECIDED:
			return winner

		# computer plays after
		position = pcMove(board)
		DoMove(board, GameEnum.PLAYER_COMPUTER, position)

		winner = GetGameWinner(board)
		if winner != GameEnum.GAME_UNDECIDED:
			return winner

def pcMove(board):
	#return AlphaBeta.Search(board)
	return MiniMax.Decision(board)
	
######################################
class AlphaBeta:
	@staticmethod
	def Search(state):
		value, playMove = AlphaBeta.MaxValue_Init(state, GameEnum.MIN_INT, GameEnum.MAX_INT)
		return playMove
		
	@staticmethod
	def MaxValue_Init(state, alfa, beta):
		assert terminalTest(state) == False
			
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
		if terminalTest(state):
			return utility(state)
			
		value = GameEnum.MAX_INT
		for s in sucessors(state, GameEnum.PLAYER_HUMAN):
			value = min(value, AlphaBeta.MaxValue(s, alfa, beta))

			if value <= alfa:
				return value

			beta = min(beta, value)
			
		return value

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

#######################################
class MiniMax:
	@staticmethod
	def Decision(state):
		value, playMove = MiniMax.maxValue_Init(state)
		return playMove
		
	@staticmethod
	def maxValue_Init(state):
		assert terminalTest(state) == False
		
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
		if terminalTest(state):
			return utility(state)
			
		value = GameEnum.MIN_INT
		for s in sucessors(state, GameEnum.PLAYER_COMPUTER):
			value = max(value, MiniMax.minValue(s))
		return value
		
	@staticmethod
	def minValue(state):
		if terminalTest(state):
			return utility(state)
		
		value = GameEnum.MAX_INT
		for s in sucessors(state, GameEnum.PLAYER_HUMAN):
			value = min(value, MiniMax.maxValue(s))
		return value

def sucessors(state, player):
	stateList = []
	for idx in range(9):
		if state[idx] == GameEnum.BOARD_UNFILLED:
			newState = copy.deepcopy(state)
			newState[idx] = player
			newState[9] = idx; # store the play move after the regular board array, in the 9th position
			stateList.append(newState)

	return stateList

def terminalTest(board):
	return GetGameWinner(board) != -1

def utility(board):
	winner = GetGameWinner(board)
	if winner == GameEnum.GAME_DRAW:
		return 0
	elif winner == GameEnum.PLAYER_COMPUTER:
		return 100
	else:
		return -100

def main():
	winner = PlayGame()
	
	assert winner != GameEnum.GAME_UNDECIDED

	if winner == GameEnum.GAME_DRAW:
		print "Draw"
	elif winner == GameEnum.PLAYER_HUMAN:
		print "Player won"
	elif winner == GameEnum.PLAYER_COMPUTER:
		print "Computer won"

if __name__ == "__main__":
	main()