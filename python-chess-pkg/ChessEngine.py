import sys, pygame
pygame.init()

size = width, height = 640, 840
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

board = pygame.Surface((width,width))
board.fill('red')
boardRect = board.get_rect()

while 1:
	#quit if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    screen.blit(board, boardRect)
    pygame.display.flip()