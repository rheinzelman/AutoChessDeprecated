import pygame
import pygame_gui


class MainMenu:
    def __init__(self, window):
        self.clock = None
        self.window_surface = window

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('lightcoral'))

        self.manager = pygame_gui.UIManager((800, 600))

        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (100, 50)),
                                                         text='Start Game', manager=self.manager)

        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 325), (100, 50)),
                                                        text='Quit Game', manager=self.manager)

        self.update()

    def update(self):
        self.clock = pygame.time.Clock()
        is_running = True

        while is_running:
            is_running = self.loop()

    def loop(self):
        is_running = True
        time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print('Start Game')
                    if event.ui_element == self.quit_button:
                        print('Quit Game')
                        is_running = False

            self.manager.process_events(event)

        self.manager.update(time_delta)

        # self.window_surface.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window_surface)

        pygame.display.update()

        return is_running
