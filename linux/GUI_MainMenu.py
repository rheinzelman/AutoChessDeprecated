import pygame
import pygame_gui
import GUI_Settings
import GUI_VSChessBot
import GUI_ConnectMenu


class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('grey'))

        font = pygame.font.SysFont('montserrat.ttf', 200)
        self.text = font.render('', True, (255, 255, 255))
        self.image = pygame.image.load('logo.png')
        self.image2 = pygame.image.load('background.jpg')
        self.image3 = pygame.image.load('vscpu.png')
        self.board100 = pygame.image.load('board100.png')
        self.manager = pygame_gui.UIManager((800, 600), 'theme2.json')

        start_rect = pygame.Rect((340, 125), (150, 50))
        self.vs_cpu_button = pygame_gui.elements.UIButton(relative_rect=start_rect, text='Play vs CPU',
                                                          manager=self.manager)

        connect_rect = pygame.Rect((340, 300), (150, 50))
        self.vs_board_button = pygame_gui.elements.UIButton(relative_rect=connect_rect, text='Play vs Board',
                                                            manager=self.manager)

        settings_rect = pygame.Rect((340, 450), (150, 50))
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=settings_rect, text='Settings',
                                                            manager=self.manager)

        quit_rect = pygame.Rect((500, 450), (150, 50))
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text='Quit Game',
                                                        manager=self.manager)
       
        quit_rect = pygame.Rect((165, 450), (150, 50))
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=quit_rect, text='Friends',
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
                        if event.ui_element == self.vs_cpu_button:
                            GUI_VSChessBot.VersusCPU()
                        if event.ui_element == self.vs_board_button:
                            GUI_ConnectMenu.ConnectMenu()
                        if event.ui_element == self.settings_button:
                            GUI_Settings.SettingsMenu()
                        if event.ui_element == self.quit_button:
                            print('Quit Game')
                            is_running = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            
            self.window_surface.blit(self.image2, (0, 0))
            self.window_surface.blit(self.image3, (350, 180))
            self.window_surface.blit(self.board100, (360, 350))
            
            self.window_surface.blit(self.image, (175, 0))

            self.window_surface.blit(self.text, ((800 - self.text.get_width()) * 0.5, 50))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
