import pygame
import pygame_gui
import chessGame

class VersusCPU:
    def __init__(self):
        self.clock = None

        self.window_surface = None

        self.manager = None

        self.background = None

        self.game_space = None

        self.top_bar = None

        self.bottom_bar = None

        self.match_text = None

        self.quit_button = None

        self.flip_button = None

        self.back_button = None

        self.reset_button = None

        self.game = None

        self.setup()

        self.update()

    def setup(self):
        self.clock = pygame.time.Clock()

        self.window_surface = pygame.display.set_mode((1270, 1120))

        self.game = chessGame.ChessGame(0, 100, self.window_surface)

        self.manager = pygame_gui.UIManager((1270, 1120))

        # self.background = pygame.Surface((1270, 1120))
        # self.background.fill(pygame.Color('gray'))

        # self.game_space = pygame.Surface((1270, 920))
        # self.game_space.fill(pygame.Color('black'))

        self.top_bar = pygame.Surface((1270, 100))
        self.top_bar.fill(pygame.Color(32, 32, 32))

        self.bottom_bar = pygame.Surface((1270, 100))
        self.bottom_bar.fill(pygame.Color(32, 32, 32))

        WHITE = (255, 255, 255)

        font = pygame.font.SysFont('montserrat.ttf', 72)
        self.match_text = font.render('AI Practice Match', True, WHITE)

        quit_rect = pygame.Rect((492, 1045), (100, 50))
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text='Quit Game',
                                                        manager=self.manager)

        flip_rect = pygame.Rect((196, 1045), (100, 50))
        self.flip_button = pygame_gui.elements.UIButton(relative_rect=flip_rect, text='Flip Board',
                                                        manager=self.manager)

        back_rect = pygame.Rect((344, 1045), (100, 50))
        self.back_button = pygame_gui.elements.UIButton(relative_rect=back_rect, text='Go Back',
                                                        manager=self.manager)

        reset_rect = pygame.Rect((48, 1045), (100, 50))
        self.reset_button = pygame_gui.elements.UIButton(relative_rect=reset_rect, text='Reset Game',
                                                         manager=self.manager)

    def update(self):
        is_running = True

        while is_running:
            is_running = True
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.quit_button:
                            is_running = False
                        if event.ui_element == self.flip_button:
                            print("Flip Board")
                        if event.ui_element == self.reset_button:
                            self.setup()
                        if event.ui_element == self.back_button:
                            print("Go Back")

                self.manager.process_events(event)

            self.manager.update(time_delta)

            # self.window_surface.blit(self.background, (0, 0))

            # self.window_surface.blit(self.game_space, (0, 100))

            self.window_surface.blit(self.top_bar, (0, 0))

            self.window_surface.blit(self.bottom_bar, (0, 1020))

            self.window_surface.blit(self.match_text, (((1270 - self.match_text.get_width()) * 0.5), 25))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

            # self.game.drawGameState()

            self.game.update()

        self.game.end()

        self.window_surface = pygame.display.set_mode((800, 600))
