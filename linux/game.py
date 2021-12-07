#pygame: for window and gui creation, and board interactivity
import pygame
#chess: for move validation and match virtualization
import chess
#math: for basic math functions
import math
#time: for the illusion of the computer taking extra time to think
import time
#ioDriver.py: for communicating with the physical board's io and making the chess library output readable for the program
import ioDriver
#contains classes for utilizing chess library function calls
import gameEngine
#serial port communication library


#PYGAME DEFS
BOARD_SIZE = B_width, B_height = 920, 920
PANEL_SIZE = P_width, P_height = 350, B_height
WINDOW_SIZE = W_width, W_height = B_width + P_width, B_height #size is a tuple defined by the window height and width
dimensions = 8 #board dimensions, don't change because offsets for flipping and char conversion are hardcoded
SQUARE_SIZE = math.floor(B_height/dimensions) #size of each piece square

#image dictionary for storing images in memory for faster loading
IMAGES = {
	'b': pygame.transform.scale(pygame.image.load('piece_images/b.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'k': pygame.transform.scale(pygame.image.load('piece_images/k.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'n': pygame.transform.scale(pygame.image.load('piece_images/n.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'p': pygame.transform.scale(pygame.image.load('piece_images/p.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'q': pygame.transform.scale(pygame.image.load('piece_images/q.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'r': pygame.transform.scale(pygame.image.load('piece_images/r.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'B': pygame.transform.scale(pygame.image.load('piece_images/B.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'K': pygame.transform.scale(pygame.image.load('piece_images/K.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'N': pygame.transform.scale(pygame.image.load('piece_images/N.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'P': pygame.transform.scale(pygame.image.load('piece_images/P.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'Q': pygame.transform.scale(pygame.image.load('piece_images/Q.svg'), (SQUARE_SIZE, SQUARE_SIZE)),
	'R': pygame.transform.scale(pygame.image.load('piece_images/R.svg'), (SQUARE_SIZE, SQUARE_SIZE))
}

#Gamemode variables
GAMEMODE = 'W' # 'P' for pvp, 'W' for player vs black CPU, 'B' for player vs white CPU
CPU_DIFFICULTY = '10' #sets the difficulty of the stockfish engine, can be 1-10
'''
0: standard FEN 
1: Legal move detection
2: Endgame Checkmate
3: Promotion
4: Fivefold Repetition
5: En Passant (Set gamemode to P)
'''
DEMO_FENS = [	'',
				'4r3/2k5/2q5/8/4B3/8/1N2K1P1/8',
				'8/2k5/6R1/5R2/8/8/4K3/8',
				'4k3/6P1/1n6/8/8/6R1/1K6/8',
				'5rk1/5p1R/7K/8/8/8/8/8',
				'rnbqkbnr/1pppppp1/p6p/8/3PP3/8/PPP2PPP/RNBQKBNR']

STARTING_FEN = DEMO_FENS[5]

def main(): 
	
	pygame.init() #initialize pygame
	window = pygame.display.set_mode(WINDOW_SIZE) #set the windows size
	window.fill(pygame.Color('black')) #the window background color	
	pygame.font.init()

	#gamestate variables
	game = gameEngine.chessEngine(GAMEMODE, CPU_DIFFICULTY, STARTING_FEN) #initialize the virtual game state
	boardState = ioDriver.formatASCII(game.board) #create an array describing our boardstate
	#keeps track of where a player has clicked and stores it in player move
	playerClick = ()
	#stores 2 playerClicks and converts them into a UCI move
	playerMove = ()
	#Keeps track of turns when playing CPU
	whiteTurn = True
	isFlipped = False
	resignFlag = False
	if(GAMEMODE == 'B'):
		isFlipped = True

	#UI initialization and drawing
	font = pygame.font.SysFont('ubuntumono', 35)

	padding = 20
	
	resignButton = pygame.Rect((B_width+padding,(P_height/2)+padding, P_width*.4, P_height*.1))
	resignText = font.render('Resign', True, (200,200,200))
	
	drawButton = pygame.Rect(W_width-resignButton.w-padding, (P_height/2)+padding, P_width*.4,P_height*.1)
	drawText = font.render('Draw', True, (200,200,200))

	#display the initial boardstate before anyone makes a move
	boardState = ioDriver.formatASCII(game.board)
	drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
	drawGameState(window,game,boardState,isFlipped)

	#update the window
	pygame.display.flip()



	time.sleep(.10)
	
	running = True #game loop condition

	while running and not game.board.is_game_over() and resignFlag == False:
		
		#wait for an event to happen
		for e in pygame.event.get():
				
				#if the window is closed quit the game
				if e.type == pygame.QUIT:
					running = False
				
				#if there is a mouseclick
				elif e.type == pygame.MOUSEBUTTONDOWN: 
					
					location = pygame.mouse.get_pos() #get the coords of the mouse position
					
					#if the click is NOT on the board, then do nothing
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

		#If gamemode is vs white CPU, and it is the CPU's turn, generate a cpu move and push it
		if(GAMEMODE == 'B' and whiteTurn == True):
			if(game.pushCPUMove()):
				boardState = ioDriver.formatASCII(game.board)
				drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
				drawGameState(window,game,boardState,isFlipped)
				time.sleep(.10)
				whiteTurn = False
			else:
				print('CPU has no more legal moves')

		#if a first square and second square has been clicked, reset playerMove and check if it's valid
		if(len(playerMove) >= 4):
	
			#drawing the gamestate when there is a complete set of playerMove deletes any highlighted squares
			drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
			drawGameState(window, game, boardState, isFlipped)

			UCIMove = '' #initialize an empty string to store UCI moves

			#for every tuple in playerMove, convert it into a string and store in UCIMove
			for item in playerMove:
				UCIMove = UCIMove + str(item)
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
				boardState = ioDriver.formatASCII(game.board)
				drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
				drawGameState(window,game,boardState,isFlipped)
				if(GAMEMODE == 'B'):
					whiteTurn = not whiteTurn
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriver.formatASCII(game.board)
					drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
					drawGameState(window, game, boardState, isFlipped)					
				if(GAMEMODE == 'P'):
					isFlipped = not isFlipped
					whiteTurn = not whiteTurn
					flipTransition(window)
					drawUI(window, game, resignButton, resignText, drawButton, drawText, 'capturedPieces')
					drawGameState(window, game, boardState, isFlipped)
			playerMove = () #make playerMove empty for future moves

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
				window.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

def drawLog(window, game):
	font = pygame.font.SysFont('ubuntumono', 25)
	moveLogContainer = pygame.Rect(B_width, 0, P_width, P_height/2)
	pygame.draw.rect(window, (50,50,50), moveLogContainer)
	moveLog = game.moveLog
	movesPerRow = 4
	padding = 5
	newLineSpacing = padding
	for i in range(0, len(moveLog), movesPerRow):
		text = ''
		for j in range(movesPerRow):
			if i + j < len(moveLog):
				if((i+j)%2 == 0):
					#this line adds the move number to the beginning of every 2 elements in moveLog
					text += str(math.ceil((i+j+1)/2)) + '.'
				text += moveLog[i+j]
		moveText = font.render(text, True, (200,200,200))
		moveTextLocation = moveLogContainer.move(padding,newLineSpacing)
		window.blit(moveText,moveTextLocation)
		newLineSpacing += moveText.get_height() + 2

def drawUI(window, game, resignButton, resignText, drawButton, drawText, capturedPieces):
	sidebar = pygame.Rect(B_width,0,W_width-B_width,W_height)
	pygame.draw.rect(window, (50,50,50), sidebar)
	drawLog(window, game)
	pygame.draw.rect(window, (80,80,80), resignButton, 0, 9)
	pygame.draw.rect(window, (80,80,80), drawButton, 0, 9)
	window.blit(resignText,(resignButton.x+(resignButton.width/2)-resignText.get_width()/2, resignButton.y+(resignButton.height/2)-resignText.get_height()/2-5))
	window.blit(drawText,(drawButton.x+(drawButton.width/2)-drawText.get_width()/2, drawButton.y+(drawButton.height/2)-drawText.get_height()/2-5))



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

def offerDraw(window):
	pass
	#display a prompt asking if P2 wants to draw

def endgameScreen(window, game, resignFlag):
	pygame.draw.rect(window, (255,255,255), pygame.Rect(0,0,W_width,W_height))
	outcome = str(game.board.outcome())
	print(outcome)
	font = pygame.font.SysFont('ubuntumono', 50)
	if(resignFlag):
		outcomeText = font.render(game.getWinner() + ' won by resignation!', True, (0,0,0))
	elif('FIVEFOLD_REPETITION' in outcome):
		outcomeText = font.render('Draw by fivefold repetition!', True, (0,0,0))
	else:
		outcomeText = font.render(game.getWinner() + ' won by checkmate!', True, (0,0,0))
	window.blit(outcomeText,((W_width/2)-outcomeText.get_width()/2,(W_height/2)-outcomeText.get_height()))
	pygame.display.flip()
	time.sleep(2.5)


if __name__ == '__main__':
	main()