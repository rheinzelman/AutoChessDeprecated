import pygame
import pygame_gui
import mainMenu


activeUI = None


def main():
    pygame.init()

    pygame.display.set_caption('Quick Start')

    window_surface = pygame.display.set_mode((800, 600))

    local = mainMenu.MainMenu(window_surface)


if __name__ == '__main__':
    main()
