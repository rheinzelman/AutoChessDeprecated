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


#PYGAME DEFS
BOARD_SIZE = B_width, B_height = 640, 640
PANEL_SIZE = P_width, P_height = 350, 640
WINDOW_SIZE = W_width, W_height = B_width + P_width, 640 #size is a tuple defined by the window height and width

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
GAMEMODE = 'P' # 'P' for pvp, 'W' for player vs black CPU, 'B' for player vs white CPU
CPU_DIFFICULTY = '10' #sets the difficulty of the stockfish engine, can be 1-10

def main(): 

	print('')
	
	pygame.init() #initialize pygame
	window = pygame.display.set_mode(WINDOW_SIZE) #set the windows size
	window.fill(pygame.Color('black')) #the window background color	
	pygame.font.init()

	#gamestate variables
	game = gameEngine.chessEngine(GAMEMODE, CPU_DIFFICULTY) #initialize the virtual game state
	boardState = ioDriver.formatASCII(game.board) #create an array describing our boardstate
	#keeps track of where a player has clicked and stores it in player move
	playerClick = ()
	#stores 2 playerClicks and converts them into a UCI move
	playerMove = ()
	#Keeps track of turns when playing CPU
	whiteTurn = True
	isFlipped = False
	if(GAMEMODE == 'B'):
		isFlipped = True

	#display the initial boardstate before anyone makes a move
	boardState = ioDriver.formatASCII(game.board)
	drawGameState(window,game,boardState,isFlipped)
	pygame.display.flip()



	time.sleep(.10)
	
	running = True #game loop condition

	while running and not game.board.is_game_over():
		
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
						break
					#if the gamemode is vs black cpu or it is white's turn, get the click position like normal
					if(GAMEMODE == 'W' or (GAMEMODE == 'P' and whiteTurn == True)):
						col = chr(math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						highlightSquare(window, boardState, isFlipped, 8-math.floor(9-(location[0]/SQUARE_SIZE)), 8-row)
						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move
					#if the gamemode is vs white cpu or it is black's turn, flip the coordinate calculation
					if(GAMEMODE == 'B' or (GAMEMODE == 'P' and whiteTurn == False)):
						col = chr(7-math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = 9-math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						highlightSquare(window, boardState, isFlipped, math.floor((location[0]/SQUARE_SIZE)), row-1)
						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move

		#If gamemode is vs white CPU, and it is the CPU's turn, generate a cpu move and push it
		if(GAMEMODE == 'B' and whiteTurn == True):
			game.pushCPUMove()
			boardState = ioDriver.formatASCII(game.board)
			drawGameState(window,game,boardState,isFlipped)
			time.sleep(.10)
			whiteTurn = False

		#if a first square and second square has been clicked, reset playerMove and check if it's valid
		if(len(playerMove) >= 4):
	
			#drawing the gamestate when there is a complete set of playerMove deletes any highlighted squares
			drawGameState(window, game, boardState, isFlipped)

			UCIMove = '' #initialize an empty string to store UCI moves
			
			#for every tuple in playerMove, convert it into a string and store in UCIMove
			for item in playerMove:
				UCIMove = UCIMove + str(item)
			#if pushPlayerMove returns false (invalid move), tell the player
			if((str(playerMove[0]) + str(playerMove[1])) == (str(playerMove[2]) + str(playerMove[3]))):
				print('Deselecting move')
			elif(game.pushPlayerMove(UCIMove) == False):
				print('Illegal move!')
			#otherwise, update the boardState array, use it to update the window
			#then generate a cpu move, and update the window
			else:
				boardState = ioDriver.formatASCII(game.board)
				drawGameState(window,game,boardState,isFlipped)
				if(GAMEMODE == 'B'):
					whiteTurn = not whiteTurn
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriver.formatASCII(game.board)
					drawGameState(window, game, boardState, isFlipped)					
				if(GAMEMODE == 'P'):
					isFlipped = not isFlipped
					whiteTurn = not whiteTurn
					#flipTransition(window)
					drawGameState(window, game, boardState, isFlipped)
			playerMove = () #make playerMove empty for future moves

	endgameScreen(window, game)

	print('Move Log: ' + game.getMoveLog())
	print('Winner: ' + game.getWinner())
	print("Quitting...")
	#when exiting the game loop, quit pygame
	pygame.quit()
	#quit the chess engine
	game.quitEngine()

#update the board by calling drawSquares and drawPieces
def drawGameState(window, game, boardState, isFlipped):
	drawSquares(window)
	drawPieces(window, boardState, isFlipped)
	drawUI(window, game, 'moveLog', 'capturedPieces')
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

def drawLog(window, game, logList):
	font = pygame.font.SysFont('ubuntumono', 25)
	moveLogContainer = pygame.Rect(B_width, 0, P_width, P_height/2)
	pygame.draw.rect(window, (57,57,57), moveLogContainer)
	moveLog = game.moveLog
	movesPerRow = 4

	padding = 5
	newLineSpacing = padding
	for i in range(0, len(moveLog), movesPerRow):

		text = ''
		for j in range(movesPerRow):
			if i + j < len(moveLog):
				text += moveLog[i+j]
		moveText = font.render(text, True, (200,200,200))
		moveTextLocation = moveLogContainer.move(padding,newLineSpacing)
		window.blit(moveText,moveTextLocation)
		newLineSpacing += moveText.get_height() + 2

def drawUI(window, game, moveLog, capturedPieces):
	UIPos = (W_width-(W_width - B_width), 0)
	
	sidebar = pygame.Rect(UIPos[0],UIPos[1],W_width-B_width,W_height)
	pygame.draw.rect(window, (175,175,175), sidebar)

	drawLog(window, game, 'test')

def highlightSquare(window, boardState, isFlipped, col, row):
	pygame.draw.rect(window, pygame.Color(252, 189, 53), pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
	drawPieces(window, boardState, isFlipped)
	pygame.display.flip()

#a small fade to black will occur when flipping the board
def flipTransition(window):
	time.sleep(.5)
	pygame.draw.rect(window, (0,0,0), pygame.Rect(0,0,B_width,B_height))
	pygame.display.flip()
	time.sleep(.5)

def endgameScreen(window, game):
	pygame.draw.rect(window, (255,255,255), pygame.Rect(0,0,W_width,W_height))
	
	font = pygame.font.SysFont('ubuntumono', 50)
	outcomeText = font.render(game.getWinner() + ' Won!', True, (0,0,0))
	window.blit(outcomeText,((W_width/2)-outcomeText.get_width()/2,(W_height/2)-outcomeText.get_height()))
	pygame.display.flip()
	time.sleep(5)

if __name__ == '__main__':
	main()
