import pygame
import pygame_gui
import GUI_Settings
import GUI_VSChessBot


class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('lightcoral'))

        font = pygame.font.SysFont('montserrat.ttf', 72)
        self.text = font.render('Auto Chess', True, (255, 255, 255))

        self.manager = pygame_gui.UIManager((800, 600))

        start_rect = pygame.Rect((340, 175), (120, 50))
        self.vs_cpu_button = pygame_gui.elements.UIButton(relative_rect=start_rect, text='Play vs CPU',
                                                          manager=self.manager)

        start_rect = pygame.Rect((340, 250), (120, 50))
        self.vs_board_button = pygame_gui.elements.UIButton(relative_rect=start_rect, text='Play vs Board',
                                                            manager=self.manager)

        settings_rect = pygame.Rect((340, 325), (120, 50))
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=settings_rect, text='Settings',
                                                            manager=self.manager)

        quit_rect = pygame.Rect((340, 400), (120, 50))
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text='Quit Game',
                                                        manager=self.manager)

        self.update()

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
                        if event.ui_element == self.vs_cpu_button or self.vs_board_button:
                            GUI_VSChessBot.VersusCPU()
                        if event.ui_element == self.settings_button:
                            GUI_Settings.SettingsMenu()
                        if event.ui_element == self.quit_button:
                            print('Quit Game')
                            is_running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))

            self.window_surface.blit(self.text, ((800 - self.text.get_width()) * 0.5, 50))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
