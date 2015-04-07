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

clear = lambda: os.system(['clear','cls'][os.name == 'nt'])

def GetBoardSymbolForSlot(board, idx):
	if board[idx] == GameEnum.BOARD_UNFILLED:
		return str(idx + 1)
	elif board[idx] == GameEnum.PLAYER_HUMAN:
		return 'X'
	elif board[idx] == GameEnum.PLAYER_COMPUTER:
		return 'O'
		
	assert False

def drawBoard(board):
	clear()
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

# MAYBE TO REMOVE
#def firstPlayer(playerA,playerB):
#	first = None
#	print "Primeiro a jogar:"
#	print "1.",playA," (0) "
#	print "2.",playB," (X) "
#	while first not in [1,2]:
#		first = int(raw_input("Escolha o primeiro a jogar"))
#	return first-1

# returns GameEnum
# 0 if draw
# 1/2 if winner 'A' or 'B', respectively
# -1 if none of the above (game in progress?)
def GetGameWinner(board):

	winner = GameEnum.GAME_DRAW; # draw by default
	if board[0] == board[1] == board[2] != GameEnum.BOARD_UNFILLED: # top line
		winner = board[0]
		
	if board[3] == board[4] == board[5] != GameEnum.BOARD_UNFILLED: # middle line
		winner = board[3]

	if board[6] == board[7] == board[8] != GameEnum.BOARD_UNFILLED: # bottom line
		winner = board[6]

	if board[0] == board[3] == board[6] != GameEnum.BOARD_UNFILLED: # left column
		winner = board[0]

	if board[1] == board[4] == board[7] != GameEnum.BOARD_UNFILLED: # middle column
		winner = board[1]

	if board[2] == board[5] == board[8] != GameEnum.BOARD_UNFILLED: # right column
		winner = board[2]

	if board[0] == board[4] == board[8] != GameEnum.BOARD_UNFILLED: # diagonal \
		winner = board[0]

	if board[2] == board[4] == board[6] != GameEnum.BOARD_UNFILLED: # diagonal /
		winner = board[2]
		
	if winner == GameEnum.GAME_DRAW: # it's either a draw or a game in progress
		for idx in range(0, 9):
			if board[idx] != 'A' and board[idx] != 'B': # there's a free position, it's a game in progress
				winner = GameEnum.GAME_UNDECIDED # set the match as in progress

	return winner

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
	return AlphaBeta.Search(board)
	
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

def minmaxDecision(board,play):
	value,state = maxValue(board)
	return state


def utility(board):
	winner = GetGameWinner(board)
	if winner == GameEnum.GAME_DRAW:
		return 0
	elif winner == GameEnum.PLAYER_COMPUTER:
		return 1
	else:
		return -1
	
def maxValue(board):
	
	if terminalTest(board):
		return utility(board,'A')
		
	maxstate = board
	value = -float('inf')
	for s in board:
		minvalue = minValue(s)
		if minvalue > value:
			value = minvalue
			maxstate = s
	return (value,maxstate)

def minValue(board):
	if terminalTest(board):
		return utility(board,'B')
		
	v = float('inf')
	for s in board:
		maxvalue = maxValue(s)
		if maxvalue < value:
			value = maxvalue
			minstate = s
	return (value,minstate)


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