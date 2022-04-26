import pygame

size = width, height = 640, 640
dimensions = 8
SQUARE_SIZE = 20

def main():
	pygame.init()

	board = pygame.Surface((SQUARE_SIZE * dimensions, SQUARE_SIZE * dimensions))
	board.fill((255,255,255))
	for x in range(0,8,2):
		for y in range(0,8,2):
			pygame.draw.rect(board, (0,0,0), (x*size,y*size, size, size))

	pygame.quit()

if __name__ == '__main__':
	main()