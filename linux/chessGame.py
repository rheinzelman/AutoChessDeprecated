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
BOARD_SIZE = B_width, B_height = 920, 920
PANEL_SIZE = P_width, P_height = 350, 920
WINDOW_SIZE = W_width, W_height = B_width + P_width, 920 #size is a tuple defined by the window height and width
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

class ChessGame:
	def __init__(self, x, y, window):
		self.position = self.x_pos, self.y_pos = x, y

		self.window = window

		# pygame.init() #initialize pygame
		# self.window = pygame.display.set_mode(WINDOW_SIZE) #set the windows size
		# self.window.fill(pygame.Color('black')) #the window background color
		pygame.font.init()

		#gamestate variables
		self.game = gameEngine.chessEngine(GAMEMODE, CPU_DIFFICULTY) #initialize the virtual game state
		self.boardState = ioDriver.formatASCII(self.game.board) #create an array describing our boardstate
		#keeps track of where a player has clicked and stores it in player move
		self.playerClick = ()
		#stores 2 self.playerClicks and converts them into a UCI move
		self.playermove = ()
		#Keeps track of turns when playing CPU
		self.whiteTurn = True
		self.isFlipped = False
		if(GAMEMODE == 'B'):
			self.isFlipped = True

		#display the initial boardstate before anyone makes a move
		self.boardState = ioDriver.formatASCII(self.game.board)
		self.drawGameState(self.window,self.game,self.boardState,self.isFlipped)
		pygame.display.flip()

	def update(self):

		time.sleep(.10)

		running = True #game loop condition

		# while running and not self.game.board.is_game_over():

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
					if(GAMEMODE == 'W' or (GAMEMODE == 'P' and self.whiteTurn == True)):
						col = chr(math.floor((location[0]-self.x_pos)/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = math.floor(9-(location[1]-self.y_pos)/SQUARE_SIZE) #translate the row into a num, 1-9
						self.playerClick = (col, row) #make a tuple self.playerClick and have it be the row and col
						self.highlightSquare(self.window, self.boardState, self.isFlipped, 8-math.floor(9-(location[0]/SQUARE_SIZE)), 8-row)
						self.playermove = self.playermove + self.playerClick #make the self.playermove tuple nest two self.playerClick tuples, which will represent the UCI move
					#if the gamemode is vs white cpu or it is black's turn, flip the coordinate calculation
					if(GAMEMODE == 'B' or (GAMEMODE == 'P' and self.whiteTurn == False)):
						col = chr(7-math.floor((location[0]-self.x_pos)/SQUARE_SIZE)+97) #translate the column position into a char, a-h
						row = 9-math.floor(9-(location[1]-self.y_pos)/SQUARE_SIZE) #translate the row into a num, 1-9
						self.playerClick = (col, row) #make a tuple self.playerClick and have it be the row and col
						self.highlightSquare(self.window, self.boardState, self.isFlipped, math.floor((location[0]/SQUARE_SIZE)), row-1)
						self.playermove = self.playermove + self.playerClick #make the self.playermove tuple nest two self.playerClick tuples, which will represent the UCI move

		#If gamemode is vs white CPU, and it is the CPU's turn, generate a cpu move and push it
		if(GAMEMODE == 'B' and self.whiteTurn == True):
			self.game.pushCPUMove()
			self.boardState = ioDriver.formatASCII(self.game.board)
			self.drawGameState(self.window,self.game,self.boardState,self.isFlipped)
			time.sleep(.10)
			self.whiteTurn = False

		#if a first square and second square has been clicked, reset self.playermove and check if it's valid
		if(len(self.playermove) >= 4):

			#drawing the gamestate when there is a complete set of self.playermove deletes any highlighted squares
			self.drawGameState(self.window, self.game, self.boardState, self.isFlipped)

			UCIMove = '' #initialize an empty string to store UCI moves

			#for every tuple in self.playermove, convert it into a string and store in UCIMove
			for item in self.playermove:
				UCIMove = UCIMove + str(item)
			#if pushself.playermove returns false (invalid move), tell the player
			if((str(self.playermove[0]) + str(self.playermove[1])) == (str(self.playermove[2]) + str(self.playermove[3]))):
				print('Deselecting move')
			elif (self.game.pushPlayerMove(UCIMove) == False):
				print('Illegal move!')
			#otherwise, update the self.boardState array, use it to update the window
			#then generate a cpu move, and update the window
			else:
				self.boardState = ioDriver.formatASCII(self.game.board)
				self.drawGameState(self.window,self.game,self.boardState,self.isFlipped)
				if(GAMEMODE == 'B'):
					self.whiteTurn = not self.whiteTurn
				if(GAMEMODE == 'W'):
					self.game.pushCPUMove()
					self.boardState = ioDriver.formatASCII(self.game.board)
					self.drawGameState(self.window, self.game, self.boardState, self.isFlipped)
				if(GAMEMODE == 'P'):
					self.isFlipped = not self.isFlipped
					self.whiteTurn = not self.whiteTurn
					self.flipTransition(self.window)
					self.drawGameState(self.window, self.game, self.boardState, self.isFlipped)
			self.playermove = () #make self.playermove empty for future moves

		return running and not self.game.board.is_game_over()

	def end(self):
		self.endgameScreen(self.window, self.game)

		print('Move Log: ' + self.game.getMoveLog())
		print('Winner: ' + self.game.getWinner())
		print("Quitting...")
		#when exiting the game loop, quit pygame
		pygame.quit()
		#quit the chess engine
		self.game.quitEngine()

	#update the board by calling drawSquares and drawPieces
	def drawGameState(self, window, game, boardState, isFlipped):
		self.drawSquares(window)
		self.drawPieces(window, boardState, isFlipped)
		self.drawUI(window, game, 'moveLog', 'capturedPieces')
		pygame.display.flip()

	#draw squares of alternating color on the board surface by drawing a rectangle of SQUARE_SIZE
	#positions are determined by multiplying the row and column value with the square size
	def drawSquares(self, window):
		altColor = False
		for row in range(dimensions):
			altColor = not altColor
			for col in range(dimensions):
				if(altColor):
					color = pygame.Color('white')
				else: color = pygame.Color(224, 116, 108)
				altColor = not altColor
				pygame.draw.rect(window, color, pygame.Rect(self.x_pos + col*SQUARE_SIZE,self.y_pos + row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

	#draw pieces on the board by getting the piece notation from the self.boardState,
	#then blit the corresponding image using the notation as a dicitonary key
	#then space out the blits in the same manner as drawing the squares
	def drawPieces(self, window, boardState, isFlipped):
		for row in range(dimensions):
			for col in range(dimensions):
				if(not isFlipped):
					piece = boardState[row][col]
				if(isFlipped):
					piece = boardState[7-row][7-col]
				if piece != '.':
					window.blit(IMAGES[piece], pygame.Rect(self.x_pos + col*SQUARE_SIZE,self.y_pos + row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

	def drawLog(self, window, game):
		font = pygame.font.SysFont('ubuntumono', 25)
		moveLogContainer = pygame.Rect(self.x_pos + B_width, self.y_pos, P_width, P_height/2)
		pygame.draw.rect(window, (57,57,57), moveLogContainer)
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

	def drawUI(self, window, game, moveLog, capturedPieces):

		padding = 20

		sidebar = pygame.Rect(self.x_pos + B_width,self.y_pos,W_width-B_width,W_height)
		pygame.draw.rect(window, (57,57,57), sidebar)
		self.drawLog(window, game)
		resignButton = pygame.Rect((self.x_pos + B_width+padding, self.y_pos + (P_height/2)+padding, P_width*.4, P_height*.1))
		pygame.draw.rect(window, (255,0,0), resignButton, 0, 9)
		drawButton = pygame.Rect(self.x_pos + W_width-resignButton.w-padding, self.y_pos + (P_height/2)+padding, P_width*.4,P_height*.1)
		pygame.draw.rect(window, (255,0,0), drawButton, 0, 9)

	def highlightSquare(self, window, boardState, isFlipped, col, row):
		pygame.draw.rect(window, pygame.Color(252, 189, 53), pygame.Rect(self.x_pos + col*SQUARE_SIZE,self.y_pos + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		self.drawPieces(window, boardState, isFlipped)
		pygame.display.flip()

	#a small fade to black will occur when flipping the board
	def flipTransition(self, window):
		time.sleep(.5)
		pygame.draw.rect(window, (0,0,0), pygame.Rect(self.x_pos,self.y_pos,B_width,B_height))
		pygame.display.flip()
		time.sleep(.25)

	def endgameScreen(self, window, game):
		pygame.draw.rect(window, (255,255,255), pygame.Rect(self.x_pos,self.y_pos,W_width,W_height))

		font = pygame.font.SysFont('ubuntumono', 50)
		outcomeText = font.render(game.getWinner() + ' Won!', True, (0,0,0))
		window.blit(outcomeText,self.x_pos + ((W_width/2)-outcomeText.get_width()/2,self.y_pos + (W_height/2)-outcomeText.get_height()))
		pygame.display.flip()
		time.sleep(5)

# if __name__ == '__main__':
# 	main()
