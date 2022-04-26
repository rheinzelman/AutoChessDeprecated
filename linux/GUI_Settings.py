import pygame
import pygame_gui


class SettingsMenu:
    def __init__(self):
        self.resolution = None
        self.start_side = None
        self.flipped_board = None

        self.clock = pygame.time.Clock()
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('lightcoral'))

        self.manager = pygame_gui.UIManager((800, 600))

        WHITE = (255, 255, 255)

        font = pygame.font.SysFont('montserrat.ttf', 72)
        self.title_text = font.render('Settings', True, WHITE)

        main_menu_rect = pygame.Rect((300, 125), (200, 50))
        self.main_menu_button = pygame_gui.elements.UIButton(relative_rect=main_menu_rect, text='Return to Main Menu',
                                                             manager=self.manager)

        font = pygame.font.SysFont('montserrat.ttf', 24)
        self.resolution_text = font.render('Resolution', True, WHITE)

        resolution_rect = pygame.Rect((150, 250), (100, 25))
        self.resolution_list = pygame_gui.elements.UIDropDownMenu(relative_rect=resolution_rect,
                                                                  starting_option='640x480',
                                                                  options_list=['640x480',
                                                                                '1280x720',
                                                                                '1920x1080',
                                                                                '2560x1440',
                                                                                '3840x2160'],
                                                                  manager=self.manager)

        font = pygame.font.SysFont('montserrat.ttf', 24)
        self.start_side_text = font.render('Start Side', True, WHITE)

        start_side_rect = pygame.Rect((350, 250), (100, 25))
        self.start_side_list = pygame_gui.elements.UIDropDownMenu(relative_rect=start_side_rect,
                                                                  starting_option='White',
                                                                  options_list=['White',
                                                                                'Black'],
                                                                  manager=self.manager)

        font = pygame.font.SysFont('montserrat.ttf', 24)
        self.flipped_board_text = font.render('Flipped Board', True, WHITE)

        flipped_side_rect = pygame.Rect((550, 250), (100, 25))
        self.flipped_side_rect = pygame_gui.elements.UIDropDownMenu(relative_rect=flipped_side_rect,
                                                                    starting_option='Yes',
                                                                    options_list=['Yes',
                                                                                  'No'],
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
                        if event.ui_element == self.main_menu_button:
                            is_running = False
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.resolution_list:
                            self.resolution = event.text
                        if event.ui_element == self.start_side_list:
                            self.start_side = event.text
                        if event.ui_element == self.resolution_list:
                            self.flipped_board = event.text

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))

            self.window_surface.blit(self.title_text, ((800 - self.title_text.get_width()) * 0.5, 50))

            self.window_surface.blit(self.resolution_text,
                                     (150 + ((100 - self.resolution_text.get_width()) * 0.5), 225))

            self.window_surface.blit(self.start_side_text,
                                     (350 + ((100 - self.start_side_text.get_width()) * 0.5), 225))

            self.window_surface.blit(self.flipped_board_text,
                                     (550 + ((100 - self.flipped_board_text.get_width()) * 0.5), 225))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
