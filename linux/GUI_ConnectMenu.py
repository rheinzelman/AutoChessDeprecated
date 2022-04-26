import pygame
import pygame_gui


class ConnectMenu:
    def __init__(self):
        self.ip_connection = None

        self.clock = pygame.time.Clock()
        self.window_surface = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color('lightcoral'))

        self.manager = pygame_gui.UIManager((800, 600))

        WHITE = (255, 255, 255)

        font = pygame.font.SysFont('montserrat.ttf', 24)
        self.ip_field_text = font.render('Board IP Address', True, WHITE)

        ip_rect = pygame.Rect((350, 188), (100, 25))
        self.ip_field = pygame_gui.elements.UITextEntryLine(relative_rect=ip_rect, manager=self.manager)

        connect_rect = pygame.Rect((350, 225), (100, 50))
        self.connect_button = pygame_gui.elements.UIButton(relative_rect=connect_rect, text='Quit Game',
                                                           manager=self.manager)

        quit_rect = pygame.Rect((350, 765), (275, 50))
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
                        if event.ui_element == self.quit_button:
                            is_running = False
                        if event.ui_element == self.connect_button:
                            print("Connect to: " + self.ip_connection)
                    if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                        self.ip_connection = event.text

                self.manager.process_events(event)

                self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))

            self.window_surface.blit(self.ip_field_text, (((800 - self.ip_field_text.get_width()) * 0.5), 150))

            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

