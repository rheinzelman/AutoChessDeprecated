'''
make move = user input
if move is legal, push()
if not, ask for more input

'''
#used for the sleep functions to simulate the CPU taking time to move
import time
#the main chess library for move validation and gamestate checking
import chess
#The engine package allows us to integrate stockfish as a CPU opponent
import chess.engine
#this allows for an SVG rendering of the board state
import chess.svg
#defines the engine object that will be used to generate CPU moves
engine = chess.engine.SimpleEngine.popen_uci('src/stockfish')

#split() helps us break the board's ascii output into a 2d array for gui utilization
def split(ASCIIBoard):
    return [char for char in ASCIIBoard]

#initialize a new Board state called board
board = chess.Board()

#keep track if the player has resigned
resignFlag = False

#while there is no game ending condition, or the player has not resigned, continue normal play
while(board.is_game_over() == False and resignFlag == False):
    #print the initial board state
    print(board)
    print('')
    #generate a move for the CPU
    CPUMove = engine.play(board, chess.engine.Limit(time=0.1))
    #sleep some time to give the illusion of playing a human opponent
    time.sleep(.5)
    #push the move to the board
    board.push(CPUMove.move)
    #print the board again so the player can see the CPU's move
    print(board)
    print('')
    #create a new flag for legal moves
    isLegalMove = False
    #while we have yet to receive a legal move, and the player has not resigned,
    while(isLegalMove == False and resignFlag == False):
        #take some user input
        user_input = input()
        #if the user input is not resign
        if(user_input != 'resign'):
            #create a Move.from_uci variable called move
            move = chess.Move.from_uci(user_input)
        else:
            #if the player did resign, set the resign flag to true
            resignFlag = True
            print('Player has resigned, CPU wins!')
        #if the move is in the dynamic list of legal moves,
        #set the legal move? flag to true, and push the move to the board
        if(move in board.legal_moves):
            isLegalMove = True
            board.push(move)    

    '''
    placeholder for how we will send the board's character array out for gui processing
    x= str(board)
    x = split(x)
    '''
    
engine.quit()
