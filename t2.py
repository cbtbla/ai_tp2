import os
import sys
import random

clear = lambda: os.system(['clear','cls'][os.name == 'nt'])

def drawBoard(board):
	clear()
	print ("\nTIC TAC TOE \n")
	print('\n   |   |')
	print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
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
#    alg = None
#    print "Algoritmo"
#    print "1. MiniMax"
#    print "2. Alpha-Beta"
#    while alg not in [1,2]:
#        alg = int(raw_input("Escolha o algoritmo: "))
#    return alg

# MAYBE TO REMOVE
#def firstPlayer(playerA,playerB):
#	first = None
#	print "Primeiro a jogar:"
#	print "1.",playA," (0) "
#	print "2.",playB," (X) "
#	while first not in [1,2]:
#		first = int(raw_input("Escolha o primeiro a jogar"))
#	return first-1

def isWinner(board, player):
	#Returns True if that player has won
    return ((board[0] == player and board[1] == player and board[2] == player) or 	# top line
    (board[3] == player and board[4] == player and board[5] == player) or 			# middle line
    (board[6] == player and board[7] == player and board[8] == player) or 			# bottom line
    (board[0] == player and board[3] == player and board[6] == player) or 			# left column
    (board[1] == player and board[4] == player and board[7] == player) or 			# middle column
    (board[2] == player and board[5] == player and board[8] == player) or 			# right column
    (board[0] == player and board[4] == player and board[8] == player) or 			# diagonal \
    (board[2] == player and board[4] == player and board[6] == player)) 			# diagonal /
	
def Moves(board, player, play, position):
	if (position == '1'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '2'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)			
		play+=1
	elif (position == '3'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '4'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '5'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '6'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '7'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '8'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	elif (position == '9'):
		board[int(position) - 1] = player[play%2]
		drawBoard(board)
		play+=1
	
	return board, play

def Play():
	board = ['1', '2', '3', '4', '5', '6' , '7', '8', '9']

	drawBoard(board)

	play = 0
	player = ['A', 'B']

	while (play != 9):
		print ("Player ", player[play%2])
		if (not play%2):
			position = input("Choose a number: ")
		else:
			position = pcMove(board)
			board[int(position) - 1] = player[play%2]
			drawBoard(board)
			play+=1

		board, play = Moves(board, player, play, position)

		if (isWinner(board, player[(play-1)%2])): return player[(play-1)%2]

		if (play == 9): return False

def pcMove(board):
	while (True):
		number = random.sample(board,  1)[0]
		
		try:		
			number = int(number)
			if ((number > 0) or (number < 10)):
				return number
		except:
			pass

def AllCombinations(board, play):
	allBoards = []
	#for i in range(9):
		
	
	return allBoards

def minmax(board, depth, maximizingPlayer):
	node = AllCombinations(board)
	node = []
	if (depth == 0):
		return depth
	if maximizingPlayer:
		bestValue = -float('inf')
		#foreach child in node:
		#	val = minmax(child, depth -1, False)
		#	bestValue = max(bestValue, val)
		return bestValue
	else:
		bestValue = float('inf')
		#foreach child in node:
		#	val = minmax(child, depth -1, False)
		#	bestValue = min(bestValue, val)
		return bestValue

def main():
	winner = Play()

	if (winner == False): print ("Draw")
	else: print ("The winner is player:", winner)

if __name__ == "__main__":
	main()