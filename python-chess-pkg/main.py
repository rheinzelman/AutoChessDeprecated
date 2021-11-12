import pygame
import chess
import humanVSCPU
import ioDriver


#PYGAME DEFS
WIDTH = HEIGHT = 624
DIMENSIONS = 8 
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

def loadImages():
	pieces = ['b','k','n','p','q','r','B','K','N','P','Q','R']

	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load('piece_images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def main(): 

	pygame.init() #initialize pygame
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	screen.fill(pygame.Color('white'))
	#initialize a new Board state called board
	board = chess.Board()
	boardState = ioDriver.formatASCII(board)
	loadImages()
	running = True

	while running:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				running = False
		drawGameState(screen,boardState)
		clock.tick(MAX_FPS)
		pygame.display.flip()

def drawGameState(screen, boardState):
	drawSquares(screen)
	drawPieces(screen, boardState)

def drawSquares(screen):
	colors = [pygame.Color('white'),pygame.Color(186, 214, 165)]
	for r in range(DIMENSIONS):
		for c in range(DIMENSIONS):
			color = colors[((r+c)%2)]
			pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen, boardState):
	for r in range(DIMENSIONS):
		for c in range(DIMENSIONS):
			piece = boardState[r][c]
			if piece != '.':
				screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == '__main__':
	main()
