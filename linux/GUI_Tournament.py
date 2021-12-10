#Initial imports, uses pygame for UI 
import pygame
import pygame_gui
import GUI_Settings
import GUI_VSChessBot
import GUI_ConnectMenu


class MainMenu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_surface = pygame.display.set_mode((800, 600))

        #Loading themes and basic UI elements
        self.background = pygame.Surface((800, 600))
        font = pygame.font.SysFont('montserrat.ttf', 200)
        self.text = font.render('', True, (255, 255, 255))
        self.tournaments = pygame.image.load('tournaments.png')
        self.image3 = pygame.image.load('background.jpg')
        self.manager = pygame_gui.UIManager((800, 600), 'tournament.json')

        userBank = 100; #Basic int for testing
        self.update()

    def update(self):
        is_running = True
	#Loop that runs every tick of the application. This ensures that UI 
	#elements are responsive. 
        while is_running:
            is_running = True
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
		#Handling for different buttons pressed by the user.
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.joinTournament:
                            is_running = False
                            #GUI_joinedTournament.joinedTournament()
                        if event.ui_element == self.tournamentInfo:
                            is_running = False
                            #GUI_tournamentInfo.tournamentInfo()
                        if event.ui_element == self.quit_button:
                            print('Quit Game')
                            is_running = False
		
		#Manager processing and basic GUI Elements called to screen with blit function 
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.window_surface.blit(self.image3, (0, 0))
            self.window_surface.blit(self.tournaments, (150, 0))
            self.window_surface.blit(self.text, ((800 - self.text.get_width()) * 0.5, 50))
            self.manager.draw_ui(self.window_surface)
             
            #Main function used to generate blocks of tournament data
            #Takes in a title, entry cost, logo icon, ruleset, and the current
            #value in the users account. 
            def printTournament(title, cost, logo, ruleset,userBank, elo):
            	tournamentBackground = pygame.Rect((100, 100), (150, 50))
            	self.tournamentbackground = pygame_gui.elements.UIButton(relative_rect=tournamentBackground, text=title, manager=self.manager)
            	
            	#Handles if the user can't afford the tournament.
            	if cost > userBank:
            	  tournamentBackground = pygame.Rect((100, 450), (150, 50))
            	  self.tournamentbackground = pygame_gui.elements.UIButton(relative_rect=tournamentBackground, text="Not enough balance to enter.",manager=self.manager)
            	  #Prompts the user and requests additional funds.
            	  popUp = pygame.Rect((100, 100), (50, 50))
            	  self.popUpBox = pygame_gui.windows.UIConfirmationDialog(action_long_desc="Add money to your account.",rect=popUp,action_short_name ="Add balance?",manager=self.manager)
            	
            	#Handles if the user can afford the tournament.
            	if cost < userBank:
            	  userBank = userBank - cost
            	  tournamentBackground = pygame.Rect((100, 100), (500, 100))
            	  #Prints the entrant cost to the general tournament info box.
            	  self.tournamentbackground = pygame_gui.elements.UILabel(relative_rect=tournamentBackground, text="The entrant cost is:" + str(cost),manager=self.manager)
            	  
            	  #Prints visual information about the tournament to the screen.
            	self.tournamentLogo = pygame.image.load(logo + '.svg')
            	self.window_surface.blit(self.tournamentLogo, (0, 0))
            	self.image2 = pygame.image.load('Q.svg')
            	self.window_surface.blit(self.image2, (200, 200))
            	
            	rulesetBox = pygame.Rect((100, 100), (500, 100))
            	#Prints the ruleset used for the tournament
            	self.rulesetInfo = pygame_gui.elements.UILabel(relative_rect=rulesetBox, text="The ruleset is:" + ruleset,manager=self.manager)
            	#Elo requirements handling, prompts the user to queue for a
            	#game if their elo is not high enough
            	if elo > 1000:
            	  popUp = pygame.Rect((100, 100), (50, 50))
            	  self.popUpBox = pygame_gui.windows.UIConfirmationDialog(action_long_desc="AMore elo needed.",rect=popUp,action_short_name ="Queue up?",manager=self.manager)
            	#userManager.addToQueue(elo)  
            	if elo > 1000:
            	  tourneyConfBox = pygame.Rect((100, 100), (500, 100))
            	  self.tourneyConf = pygame_gui.elements.UILabel(relative_rect=tourneyConfBox, text="You have entered the" + title + "tournament!",manager=self.manager)
            	#usermanager.addToTournament(title) 
            printTournament("Queen's Cup", 50, "Q", "Standard", 100, 1000)
            pygame.display.update()
