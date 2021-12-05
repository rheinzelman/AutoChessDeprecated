import pygame
import GUI_MainMenu
import chessGame


def main():
    pygame.init()

    pygame.display.set_caption('Quick Start')

    GUI_MainMenu.MainMenu()


if __name__ == '__main__':
    main()
