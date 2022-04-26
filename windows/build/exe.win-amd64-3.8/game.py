import os
#pygame: for window and gui creation, and board interactivity
import pygame
#chess: for move validation and match virtualization
import chess
#math: for basic math functions
import math
#time: for the illusion of the computer taking extra time to think
import time
#ioDriver.py: for communicating with the physical board's io and making the chess library output readable for the program
from ioDriver import IODriver
#contains classes for utilizing chess library function calls
import gameEngine
#serial port communication library

print("test")

#PYGAME DEFS
BOARD_SIZE = B_width, B_height = 420, 420 #size of the chess board
PANEL_SIZE = P_width, P_height = 350, B_height #size of the side panel
WINDOW_SIZE = W_width, W_height = B_width + P_width, B_height #size of the entire window
dimensions = 8 #board dimensions, don't change because offsets for flipping and char conversion are hardcoded
SQUARE_SIZE = math.floor(B_height/dimensions) #size of each piece square

#image dictionary for storing images in memory for faster loading
IMAGES = {
	'b': pygame.transform.scale(pygame.image.load('piece_images/bw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'k': pygame.transform.scale(pygame.image.load('piece_images/kw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'n': pygame.transform.scale(pygame.image.load('piece_images/nw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'p': pygame.transform.scale(pygame.image.load('piece_images/pw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'q': pygame.transform.scale(pygame.image.load('piece_images/qw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'r': pygame.transform.scale(pygame.image.load('piece_images/rw.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'bw': pygame.transform.scale(pygame.image.load('piece_images/b.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'kw': pygame.transform.scale(pygame.image.load('piece_images/k.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'nw': pygame.transform.scale(pygame.image.load('piece_images/n.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'pw': pygame.transform.scale(pygame.image.load('piece_images/p.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'qw': pygame.transform.scale(pygame.image.load('piece_images/q.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'rw': pygame.transform.scale(pygame.image.load('piece_images/r.svg'), (SQUARE_SIZE, SQUARE_SIZE))
}

#Gamemode variables
GAMEMODE = 'B' # 'P' for pvp, 'W' for player vs black CPU, 'B' for player vs white CPU
CPU_DIFFICULTY = '2' #sets the difficulty of the stockfish engine, can be 1-10
'''
0: standard FEN 
1: Legal move detection
2: Endgame Checkmate
3: Promotion
4: Fivefold Repetition
5: En Pessant (Set gamemode to P)
'''
DEMO_FENS = [	'',
				'4r3/2k5/2q5/8/4B3/8/1N2K1P1/8',
				'8/2k5/6R1/5R2/8/8/4K3/8',
				'4k3/6P1/1n6/8/8/6R1/1K6/8',
				'5rk1/5p1R/7K/8/8/8/8/8',
				'rnbqkbnr/1pppppp1/p6p/8/3PP3/8/PPP2PPP/RNBQKBNR']

STARTING_FEN = DEMO_FENS[0]

ioDriverObj = IODriver()

def main(): 
	
	pygame.init() #initialize pygame
	window = pygame.display.set_mode(WINDOW_SIZE) #set the windows size
	window.fill(pygame.Color('black')) #the window background color	

	#gamestate variables
	game = gameEngine.chessEngine(GAMEMODE, CPU_DIFFICULTY, STARTING_FEN) #initialize the virtual game state
	#initializeBoardState()
	boardState = ioDriverObj.formatASCII(game.board) #create an array describing our boardstate
	#keeps track of where a player has clicked and stores it in player move
	playerClick = ()
	#stores 2 playerClicks and converts them into a UCI move
	playerMove = ()
	whiteTurn = True #Keeps track of whose turn it is 
	isFlipped = False #Bool for flipping the board when appropriate
	resignFlag = False #Bool for exiting game loop on player resignation
	#if we're Black vs white CPU, the board will be flipped
	if(GAMEMODE == 'B'):
		isFlipped = True

	#UI initialization and drawing
	font = pygame.font.SysFont('ubuntumono', 35)

	padding = 20 #default padding for the buttons
	#resign and draw button rectangles with their appropriate text within
	resignButton = pygame.Rect((B_width+padding,(P_height/2)+padding, P_width*.4, P_height*.1))
	resignText = font.render('Resign', True, (200,200,200))
	drawButton = pygame.Rect(W_width-resignButton.w-padding, (P_height/2)+padding, P_width*.4,P_height*.1)
	drawText = font.render('Draw', True, (200,200,200))

	boardState = ioDriverObj.formatASCII(game.board) #display the initial boardstate before anyone makes a move
	drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces') #Draw the Side panel along with the UI elements
	drawGameState(window,game,boardState,isFlipped) #draw the board in the correct gamestate

	#update the window
	pygame.display.flip()

	#sleep some time before the CPU makes a move or before the player can make a move
	time.sleep(.10)
	
	running = True #game loop condition

	#while the game is running, there are no game ending conditions, and no one has resigned, execute the main loop
	while running and not game.board.is_game_over() and resignFlag == False:
		
		#wait for an event to happen
		for e in pygame.event.get():
				
				#if the window is closed quit the game
				if e.type == pygame.QUIT:
					running = False
				
				#if there is a mouseclick
				elif e.type == pygame.MOUSEBUTTONDOWN: 
					
					location = pygame.mouse.get_pos() #get the coords of the mouse position
					
					#if the click is NOT on the board, then check to see if resign or draw was clicked
					if(location[0] > B_width or location[1] > B_height):
						if(resignButton.collidepoint(location)):
							resignFlag = True
							print(game.getTurn() + ' has resigned.')
						elif(drawButton.collidepoint(location)):
							print(game.getTurn() + ' offers a draw...')
							offerDraw(window)
					#if the gamemode is vs black cpu or it is white's turn, get the click position like normal
					if((location[0] <= B_width and location[1] <= B_height) and GAMEMODE == 'W' or (GAMEMODE == 'P' and whiteTurn == True)):
						col = chr(math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						highlightSquare(window, boardState, isFlipped, 8-math.floor(9-(location[0]/SQUARE_SIZE)), 8-row)

						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move

					#if the gamemode is vs white cpu or it is black's turn, flip the coordinate calculation
					if((location[0] <= B_width and location[1] <= B_height) and GAMEMODE == 'B' or (GAMEMODE == 'P' and whiteTurn == False)):
						col = chr(7-math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = 9-math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						highlightSquare(window, boardState, isFlipped, math.floor((location[0]/SQUARE_SIZE)), row-1)
						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move

		#If gamemode is vs white CPU, and it is the CPU's turn, generate a cpu move, push it, and draw the board
		if(GAMEMODE == 'B' and whiteTurn == True):
			if(game.pushCPUMove()):
				boardState = ioDriverObj.formatASCII(game.board)
				drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
				drawGameState(window,game,boardState,isFlipped)
				time.sleep(.10)
				whiteTurn = False
			else:
				print('CPU has no more legal moves')

		#if a first square and second square has been clicked, reset playerMove and check if it's a valid move. If it is, push it to the board
		if(len(playerMove) >= 4):
	
			#drawing the gamestate when there is a complete set of playerMove deletes any highlighted squares
			drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
			drawGameState(window, game, boardState, isFlipped)

			UCIMove = '' #initialize an empty string to store UCI moves

			#for every tuple in playerMove, convert it into a string and store in UCIMove
			for item in playerMove:
				UCIMove = UCIMove + str(item)
			print(playerMove)
			#isPawnPromotion
			if(game.isPawn(playerMove) and playerMove[1] == 7 and playerMove[3] == 8):
				UCIMove = playerMove[0] + str(playerMove[1]) + playerMove[2] + str(playerMove[3]) + 'q'
			#if pushPlayerMove returns false (invalid move), tell the player
			if((str(playerMove[0]) + str(playerMove[1])) == (str(playerMove[2]) + str(playerMove[3]))):
				print('Deselecting move')
			elif(game.pushPlayerMove(UCIMove) == False):
				print('Illegal move!')
			#otherwise, update the boardState array, use it to update the window
			#then generate a cpu move, and update the window
			else:
				boardState = ioDriverObj.formatASCII(game.board)
				drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
				drawGameState(window,game,boardState,isFlipped)
				if(GAMEMODE == 'B'):
					whiteTurn = not whiteTurn
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriverObj.formatASCII(game.board)
					drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
					drawGameState(window, game, boardState, isFlipped)					
				if(GAMEMODE == 'P'):
					isFlipped = not isFlipped
					whiteTurn = not whiteTurn
					flipTransition(window)
					drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
					drawGameState(window, game, boardState, isFlipped)
			playerMove = () #make playerMove empty for future moves

	time.sleep(1)
	endgameScreen(window, game, resignFlag)
	
	#when exiting the game loop, quit pygame
	pygame.quit()
	#quit the chess engine
	game.quitEngine()

#update the board by calling drawSquares and drawPieces
def drawGameState(window, game, boardState, isFlipped):
	drawSquares(window)
	drawPieces(window, boardState, isFlipped)
	pygame.display.flip()

#draw squares of alternating color on the board surface by drawing a rectangle of SQUARE_SIZE
#positions are determined by multiplying the row and column value with the square size 
def drawSquares(window):
	altColor = False
	for row in range(dimensions):
		altColor = not altColor
		for col in range(dimensions):
			if(altColor):
				color = pygame.Color('white')
			else: color = pygame.Color(224, 116, 108)
			altColor = not altColor
			pygame.draw.rect(window, color, pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

#draw pieces on the board by getting the piece notation from the boardState, 
#then blit the corresponding image using the notation as a dicitonary key
#then space out the blits in the same manner as drawing the squares
def drawPieces(window, boardState, isFlipped):
	for row in range(dimensions):
		for col in range(dimensions):
			if(not isFlipped):
				piece = boardState[row][col]
			if(isFlipped):
				piece = boardState[7-row][7-col]
			if piece != '.':
				if piece.isupper():
					piece = piece.lower()
				else:
					piece = piece + "w"
				print(piece)
				window.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

def drawLog(window, game):
	font = pygame.font.SysFont('ubuntumono', 25) #create font object for text creation
	moveLogContainer = pygame.Rect(B_width, 0, P_width, P_height/2) #create a container for the move log
	pygame.draw.rect(window, (50,50,50), moveLogContainer) #draw the moveLogContainer to the window
	moveLog = game.moveLog #make a moveLog object that is the same as the game class' moveLog
	movesPerRow = 4 #number of moves per row in the moveLog
	padding = 5 #default padding between moves
	newLineSpacing = padding # newLine space between rows
	
	#iterate through every 4 moves
	for i in range(0, len(moveLog), movesPerRow):
		text = ''
		#iterate through moves i -> i+4
		for j in range(movesPerRow):
			#if we are not out of moves to print:
			if i + j < len(moveLog):
				#and if we are on every second move, add the move number
				if((i+j)%2 == 0):
					#this line adds the move number to the beginning of every 2 elements in moveLog
					text += str(math.ceil((i+j+1)/2)) + '.'
				#append the most recent move to the moveLog text
				text += moveLog[i+j]
		#re-render the movelog every time it gets a new move
		moveText = font.render(text, True, (200,200,200))
		moveTextLocation = moveLogContainer.move(padding,newLineSpacing)
		window.blit(moveText,moveTextLocation)
		newLineSpacing += moveText.get_height() + 2

def drawUI(window, game, resignButton, resignText, drawButton, drawText, capturedPieces):
	#make a Rect variable sidebar that is located on the right side of the board and is the same height as the board, and W_width - B_width in width
	sidebar = pygame.Rect(B_width,0,W_width-B_width,W_height)
	#draw the sidebar container
	pygame.draw.rect(window, (50,50,50), sidebar)
	#draw our moveLog
	drawLog(window, game)
	#create containers for the resign and draw buttons
	pygame.draw.rect(window, (80,80,80), resignButton, 0, 9)
	pygame.draw.rect(window, (80,80,80), drawButton, 0, 9)
	#render the buttons onto the sidebar surface
	window.blit(resignText,(resignButton.x+(resignButton.width/2)-resignText.get_width()/2, resignButton.y+(resignButton.height/2)-resignText.get_height()/2-5))
	window.blit(drawText,(drawButton.x+(drawButton.width/2)-drawText.get_width()/2, drawButton.y+(drawButton.height/2)-drawText.get_height()/2-5))


#change the color of the most recently clicked board square
def highlightSquare(window, boardState, isFlipped, col, row):
	pygame.draw.rect(window, pygame.Color(252, 189, 53), pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
	drawPieces(window, boardState, isFlipped)
	pygame.display.flip()

#a small fade to black will occur when flipping the board
def flipTransition(window):
	time.sleep(.5)
	pygame.draw.rect(window, (0,0,0), pygame.Rect(0,0,B_width,B_height))
	pygame.display.flip()
	time.sleep(.25)

#WIP
def offerDraw(window):
	pass
	#display a prompt asking if P2 wants to draw

#Display an endgame splash screen with details of who won
def endgameScreen(window, game, resignFlag):
	#draw a surface covering the entire window
	pygame.draw.rect(window, (255,255,255), pygame.Rect(0,0,W_width,W_height))
	#create an outcome string with board.outcome() data
	outcome = str(game.board.outcome())
	print(outcome)
	font = pygame.font.SysFont('ubuntumono', 50)
	#if a user resigned, display the appropriate winner
	if(resignFlag):
		outcomeText = font.render(game.getWinner() + ' won by resignation!', True, (0,0,0))
	#if fivefold repition happened, display that there was a draw
	elif('FIVEFOLD_REPETITION' in outcome):
		outcomeText = font.render('Draw by fivefold repetition!', True, (0,0,0))
	#else, a checkmate has happened
	else:
		outcomeText = font.render(game.getWinner() + ' won by checkmate!', True, (0,0,0))
	window.blit(outcomeText,((W_width/2)-outcomeText.get_width()/2,(W_height/2)-outcomeText.get_height()))
	pygame.display.flip()
	time.sleep(2.5)


if __name__ == '__main__':
	main()