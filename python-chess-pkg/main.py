import pygame
<<<<<<< Updated upstream
=======
import pygame_menu
>>>>>>> Stashed changes
import chess
import humanVSCPU
import ioDriver


#PYGAME DEFS
WIDTH = HEIGHT = 624
DIMENSIONS = 8 
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

<<<<<<< Updated upstream
=======
#Gamemode variable, 'P' for pvp, 'W' for vs black cpu, 'B' for vs white cpu
GAMEMODE = 'B'

#create an array of pieces names,
#in our image dictionary, define each piece to be the appropriate chess piece image loaded into mem
>>>>>>> Stashed changes
def loadImages():
	pieces = ['b','k','n','p','q','r','B','K','N','P','Q','R']

	for piece in pieces:
		IMAGES[piece] = pygame.transform.scale(pygame.image.load('piece_images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def main(): 
<<<<<<< Updated upstream

	pygame.init() #initialize pygame
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	screen.fill(pygame.Color('white'))
	#initialize a new Board state called board
	board = chess.Board()
	boardState = ioDriver.formatASCII(board)
	loadImages()
	running = True
=======
	pygame.init() #initialize pygame
	main_menu = pygame.display.set_mode((600,400))
	game = versusCPU.CPUClass(GAMEMODE) #for now we are just initializing versusCPU game
	screen = pygame.display.set_mode(size) #set the windows size
	clock = pygame.time.Clock() #set our tick rate
	screen.fill(pygame.Color('black')) #the window background color	
	boardState = ioDriver.formatASCII(game.board) #create an array describing our boardstate
	loadImages() #load all the chess images into mem
	running = True #pygame good practice
	playerClick = ()
	playerMove = ()
	CPUTurn = False
	if(GAMEMODE == 'B'):
		CPUTurn = True

	while running:		
>>>>>>> Stashed changes

	while running:
		for e in pygame.event.get():
<<<<<<< Updated upstream
			if e.type == pygame.QUIT:
				running = False
=======
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

		if(GAMEMODE == 'B' and CPUTurn == True):
			game.pushCPUMove()
			boardState = ioDriver.formatASCII(game.board)
			drawGameState(screen,boardState)
			pygame.display.flip()
			CPUTurn = False

		#if a first square and second square has been clicked, reset playerMove and check if it's valid
		if(len(playerMove) >= 4):
			UCIMove = ''
			#transform the playerMove tuple into a cohesive UCIMove string for proper pushPlayerMove parsing
			for item in playerMove:
				UCIMove = UCIMove + str(item)
			playerMove = ()
			#if the move cannot be legally pushed, then pass and continue waiting for a move
			if(game.pushPlayerMove(UCIMove) == False):
				pass
			else:
				boardState = ioDriver.formatASCII(game.board)
				drawGameState(screen,boardState)
				pygame.display.flip()
				CPUTurn = True
				if(GAMEMODE == 'W'):
					game.pushCPUMove()
					boardState = ioDriver.formatASCII(game.board)

>>>>>>> Stashed changes
		drawGameState(screen,boardState)
		clock.tick(MAX_FPS)
		pygame.display.flip()

<<<<<<< Updated upstream
=======
	pygame.quit()

def mode_select(GAMEMODE):
	pass

def CPU_difficulty_select():
	pass

def mainMenu():
	menu = pygame_menu.Menu('Welcome', 400,300,
		theme=pygame_menu.themes.THEME_BLUE)

	menu.add.text_input('Name :', default='John Doe')
	menu.add.selector('Game Mode', [('Player vs Player', 1), ('Player vs Black CPU', 2), ('Player vs White CPU', 3)], onchange=mode_select)
	menu.add.selector('CPU Difficulty', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=CPU_difficulty_select)
	menu.add.button('Play', pygame_menu.events.EXIT)
	menu.add.button('Quit', pygame_menu.events.EXIT)

>>>>>>> Stashed changes
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
