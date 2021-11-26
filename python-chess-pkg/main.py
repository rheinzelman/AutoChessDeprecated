import pygame
import sys
import chess
import time
import math
import ioDriver
import versusCPU


#PYGAME DEFS
size = width, height = 1024, 1024 #size is a tuple defined by the window height and width
dimensions = 8 #board dimensions
SQ_SIZE = math.floor(height/dimensions) #size of each piece square
MAX_FPS = 15 #tick rate for the game
IMAGES = {} #image dictionary for storing images in memory for faster loading

#Gamemode variable, 'P' for pvp, 'W' for vs black cpu, 'B' for vs white cpu
GAMEMODE = 'W'

#create an array of pieces names,
#in our image dictionary, define each piece to be the appropriate chess piece image loaded into mem
def loadImages():
	pieces = ['b','k','n','p','q','r','B','K','N','P','Q','R']
	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load('piece_images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def main(): 
	pygame.init() #initialize pygame
	game = versusCPU.CPUClass(GAMEMODE) #for now we are just initializing versusCPU game
	screen = pygame.display.set_mode(size) #set the windows size
	clock = pygame.time.Clock() #set our tick rate
	screen.fill(pygame.Color('black')) #the window background color	
	boardState = ioDriver.formatASCII(game.board) #create an array describing our boardstate
	loadImages() #load all the chess images into mem
	running = True #pygame good practice
	playerClick = ()
	playerMove = ()
	while running:

		#if player color is black, let cpu move first
		if(GAMEMODE == 'B'):
			game.pushCPUMove()
			boardState = ioDriver.formatASCII(game.board)

		#wait for an event to happen
		for e in pygame.event.get():
				#if the window is closed quit the game
				if e.type == pygame.QUIT:
					running = False
				#if there is a mouseclick
				elif e.type == pygame.MOUSEBUTTONDOWN: 

					location = pygame.mouse.get_pos() #get the coords of the mouse position
					col = chr(math.floor(location[0]/SQ_SIZE)+97) #translate the column position into a char, a-h
					row = math.floor(9-location[1]/SQ_SIZE) #translate the row into a num, 1-9
					playerClick = (col, row) #make a tuple playerClick and have it be the row and col
					playerMove = playerMove + playerClick #make the playerMove tuple nest two playerClick tuples, which will represent the UCI move

		#if a first square and second square has been clicked, reset playerMove and check if it's valid
		if(len(playerMove) >= 4):
			UCIMove = ''
			for item in playerMove:
				UCIMove = UCIMove + str(item)
			playerMove = ()
			if(game.pushPlayerMove(UCIMove) == False):
				pass
			else:
				boardState = ioDriver.formatASCII(game.board)
				drawGameState(screen,boardState)
				pygame.display.flip()
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriver.formatASCII(game.board)

		drawGameState(screen,boardState)
		clock.tick(MAX_FPS)
		pygame.display.flip()

	pygame.quit()

def drawGameState(screen, boardState):
	drawSquares(screen)
	drawPieces(screen, boardState)

def drawSquares(screen):
	colors = [pygame.Color('white'),pygame.Color(186, 214, 165)]
	for r in range(dimensions):
		for c in range(dimensions):
			color = colors[((r+c)%2)]
			pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen, boardState):
	for r in range(dimensions):
		for c in range(dimensions):
			piece = boardState[r][c]
			if piece != '.':
				screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == '__main__':
	main()
