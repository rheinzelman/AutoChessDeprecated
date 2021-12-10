Installation:
Currently tested and working on linux with python3. Dependencies need to be installed through pip. Dependencies needed are: 
 - chess
 - pygame 
Once these libraries are installed, run main.py with 'python3 game.py'

Overview:

To fully understand what's going on within the chess and pygame function calls, it's best to read the documentation on their respective websites.

There are three gamemodes, player vs player, player vs black CPU, player vs white CPU, and is chosen through the GAMEMODE variable ('P', 'W', and 'B' respectively)

All piece images are loaded into memory through a dictionary with the notation (Q,K,N,P being white's queen, king, knight, and pawn) of each piece as a key to the respective image.

drawGameState():
The board is drawn through pygame by first creating a black screen with the dimensions depending on the global variable 'size'. The game state is drawn at the beginning of a game, and after each move, with varying conditions determined by the gamemode. Drawing the gamestate is done as follows:

1. Draw the squares by iterating through both the rows and columns of the board (in this case 8 for each)in a nested loop, and each time draw an alternating colored rectangle, whose size is determined by SQUARE_SIZE, positioned by multiply the row and column with SQUARE_SIZE.  

2. Draw the pieces in the same manner as the squares, and blit the piece images to their positions by using the board notation as a key to the images dictionary created earlier.

Main Loop: 

Pygame is initialized along with all the windows. A gameEngine object is created with the GAMEMODE and CPU_DIFFICULTY passed as parameters, and will be used to keep track of the board state using the chess library, and to generate CPU moves using stockfish. 

A 2d array called boardState is created which will contain the position of all pieces using this notation: 

b bishop
k king
n knight
p pawn
q queen
r rook

with lowercase representing the black pieces, and vice versa. 

Player clicks are calculated through pygame's get_pos() function. On MOUSEBUTTONDOWN, x and y position of the cursor is stored into a playerClick tuple. This tuple, with each element containing the x and y position, are then added to the to the playerMove tuple. Once the playerMove tuple contains two sets of 'moves' (two clicks on any square) it will test the legality of the move, and if it is legal it will push it to the virtual board as well as to the chess engine to generate the opposing color's best move if playing versus a CPU.

Additionally, clicks done outside of the board are run through a .collidepoint() method which detects if any containers are being clicked, and in our case the only containers outside of the board are for the draw and resign buttons, which currently have limited functionality. 

Overall, the game loops in this manner:
1. If the gamemode is 'B', and it is white's turn, generate and push a white cpu move
2. otherwise wait for a legal player move
3a. if gamemode is 'B', flip whiteTurn bool so that the cpu may make a move at the beginning of the loop
3b. if gamemode is 'W', generate and push a cpu move.
3c. if gamemode is 'P', flip the board and it's inputs

Below the main loop are some functions that serve to facilitate pygame window and GUI creation. Most of the actualy 'game' is kept track of inside of gameEngine.py, which we will now go over. 

gameEngine module keeps track of the virtualized chess game. Move must both be pushed to the chess.Board object, as well as the stockfish engine object, so that both can run parallel games. Fairly straightforward. 

Lastly, the ioDriver module is used to convert python-chess' ugly print(Board) output and make it readable for the pygame gui we created. Essentially, it creates a 8x8 2d array that contains a char representing each piece on the board, and deletes all the fluff that print(Board) can produce. In the future, this will be used to communicate with the hardware board as well.

Contributions:
Raymond Heinzelman: game.py*, gameEngine.py, ioDriver.py
Holden Bowman - branch Holden: mainMenuTest.py, GUI_MainMenu.py, GUI_ConnectMenu.py, GUI_Settings.py, GUI_VSChessBot.py
Cade Hockersmith - branch Cade: GUI_Tournament.py, TournamentMenu.py, Updated GUI_MainMenu, Designed logos and screens

*The methods drawSquares(), drawPieces(), and parts of drawLog are based of off Eddie Sharick's tutorial video 'Chess Engine in Python - Part 1 - Drawing the board'. However, they are very modified, and serve only as a foundation for which I used to implement the rest of the program's features.

Integrated Resources:
Stockfish: https://stockfishchess.org/

Python-Chess library: https://python-chess.readthedocs.io/en/latest/


