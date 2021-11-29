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
size = width, height = 640, 640 #size is a tuple defined by the window height and width
dimensions = 8 #board dimensions
SQUARE_SIZE = math.floor(height/dimensions) #size of each piece square
IMAGES = {} #image dictionary for storing images in memory for faster loading

#Gamemode variables
GAMEMODE = 'B' # 'P' for pvp, 'W' for player vs black CPU, 'B' for player vs white CPU
CPU_DIFFICULTY = '1' #sets the difficulty of the stockfish engine, can be 1-10

#create an array of pieces names,
#in our image dictionary, define each piece to be the appropriate chess piece image loaded into mem
def loadImages():
	pieces = ['b','k','n','p','q','r','B','K','N','P','Q','R']
	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load('piece_images/' + piece + '.png'), (SQUARE_SIZE, SQUARE_SIZE))

def main(): 
	
	pygame.init() #initialize pygame
	screen = pygame.display.set_mode(size) #set the windows size
	screen.fill(pygame.Color('black')) #the window background color	
	loadImages() #load all the chess images into mem
	
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
	drawGameState(screen,boardState,isFlipped)
	pygame.display.flip()
	time.sleep(.10)
	
	running = True #game loop condition

	while running:
		
		#wait for an event to happen
		for e in pygame.event.get():
				
				#if the window is closed quit the game
				if e.type == pygame.QUIT:
					running = False
				
				#if there is a mouseclick
				elif e.type == pygame.MOUSEBUTTONDOWN: 
					#if the gamemode is vs black cpu or it is white's turn, get the click position like normal
					if(GAMEMODE == 'W' or (GAMEMODE == 'P' and whiteTurn == True)):
						location = pygame.mouse.get_pos() #get the coords of the mouse position
						col = chr(math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move
					#if the gamemode is vs white cpu or it is black's turn, flip the coordinate calculation
					if(GAMEMODE == 'B' or (GAMEMODE == 'P' and whiteTurn == False)):
						location = pygame.mouse.get_pos() #get the coords of the mouse position
						col = chr(7-math.floor(location[0]/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = 9-math.floor(9-location[1]/SQUARE_SIZE) #translate the row into a num, 1-9
						playerClick = (col, row) #make a tuple playerClick and have it be the row and col
						playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move

		#If gamemode is vs white CPU, and it is the CPU's turn, generate a cpu move and push it
		if(GAMEMODE == 'B' and whiteTurn == True):
			game.pushCPUMove()
			boardState = ioDriver.formatASCII(game.board)
			drawGameState(screen,boardState,isFlipped)
			pygame.display.flip()
			time.sleep(.10)
			whiteTurn = False

		#if a first square and second square has been clicked, reset playerMove and check if it's valid
		if(len(playerMove) >= 4):
	
			UCIMove = '' #initialize an empty string to store UCI moves
			
			#for every tuple in playerMove, convert it into a string and store in UCIMove
			for item in playerMove:
				UCIMove = UCIMove + str(item)
			#if pushPlayerMove returns false (invalid move), tell the player
			if((str(playerMove[0]) + str(playerMove[1])) == (str(playerMove[2]) + str(playerMove[3]))):
				print('Deselecting move')
			elif(game.pushPlayerMove(UCIMove) == False):
				print('Illegal move!')
			#otherwise, update the boardState array, use it to update the screen
			#then generate a cpu move, and update the screen
			else:
				boardState = ioDriver.formatASCII(game.board)
				drawGameState(screen,boardState,isFlipped)
				pygame.display.flip()
				if(GAMEMODE == 'B'):
					whiteTurn = not whiteTurn
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriver.formatASCII(game.board)
				if(GAMEMODE == 'P'):
					isFlipped = not isFlipped
					whiteTurn = not whiteTurn
			playerMove = () #make playerMove empty for future moves
			print('whiteTurn: ' + str(whiteTurn))

		#update the screen
		drawGameState(screen,boardState,isFlipped)
		pygame.display.flip()

	#when exiting the game loop, quit pygame
	pygame.quit()

#update the board by calling drawSquares and drawPieces
def drawGameState(screen, boardState,isFlipped):
	drawSquares(screen)
	drawPieces(screen, boardState, isFlipped)

#draw the squares on the board surface
def drawSquares(screen):
	altColor = False
	colors = [pygame.Color('white'),pygame.Color(224, 116, 108)]
	for row in range(dimensions):
		altColor = not altColor
		for col in range(dimensions):
			if(altColor):
				color = colors[0]
			else: color = colors[1]
			altColor = not altColor
			pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

#draw pieces on the board
def drawPieces(screen, boardState, isFlipped):
	for row in range(dimensions):
		for col in range(dimensions):
			if(not isFlipped):
				piece = boardState[row][col]
			if(isFlipped):
				piece = boardState[7-row][7-col]
			if piece != '.':
				screen.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

if __name__ == '__main__':
	main()
