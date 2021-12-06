import pygame
import GUI_MainMenu


def main():
    pygame.init()

    pygame.display.set_caption('Quick Start')

    local = GUI_MainMenu.MainMenu()


if __name__ == '__main__':
    main()
