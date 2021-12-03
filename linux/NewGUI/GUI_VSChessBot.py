import pygame
import pygame_gui


class VersusCPU:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.window_surface = pygame.display.set_mode((640, 840))

        self.manager = pygame_gui.UIManager((640, 1000))

        self.background = pygame.Surface((640, 1000))
        self.background.fill(pygame.Color('lightblue'))

        self.game_space = pygame.Surface((640, 640))
        self.game_space.fill(pygame.Color('black'))

        self.top_bar = pygame.Surface((640, 100))
        self.top_bar.fill(pygame.Color('lightcoral'))

        self.bottom_bar = pygame.Surface((720, 100))
        self.bottom_bar.fill(pygame.Color('lightcoral'))

        WHITE = (255, 255, 255)

        self.update()

    def update(self):
        is_running = True

        while is_running:
            is_running = True
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                '''if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.main_menu_button:
                            is_running = False'''

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))

            self.window_surface.blit(self.game_space, (0, 100))

            self.window_surface.blit(self.top_bar, (0, 0))

            self.window_surface.blit(self.bottom_bar, (0, 740))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        self.window_surface = pygame.display.set_mode((800, 600))