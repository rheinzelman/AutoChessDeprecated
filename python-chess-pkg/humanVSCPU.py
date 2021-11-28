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

def startGame():
    #let the player choose which side they would like to play
    print("What side would you like to play as: (W/B)")
    while 1:
        playerColor = input()
        if(playerColor == 'W' or playerColor == 'B'):
            break
        print('Please only enter W or B')

    board = chess.Board()

    #keep track if the player has resigned
    resignFlag = False

    if(playerColor == 'W'):
        while(board.is_game_over() == False and resignFlag == False):
            print(board)
            print('')

            #create a new flag for legal moves
            isLegalMove = False
            #while we have yet to receive a legal move, and the player has not resigned,
            while(isLegalMove == False and resignFlag == False):
                #take some user input
                print('Your move: ', end='')
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
                else:
                    print('Illegal move!')
            print(board)
            print('')
            #generate a move for the CPU
            CPUMove = engine.play(board, chess.engine.Limit(time=0.1))
            #sleep some time to give the illusion of playing a human opponent
            time.sleep(.5)
            print('CPU move: ', end='')
            print(CPUMove.move)
            #push the move to the board, .move just converts into a push() readable format
            board.push(CPUMove.move)
            #print the board again so the player can see the CPU's move

    if(playerColor == 'B'):
        #while there is no game ending condition, or the player has not resigned, continue normal play
        while(board.is_game_over() == False and resignFlag == False):
            #print the initial board state
            print(board)
            print('')
            #generate a move for the CPU
            CPUMove = engine.play(board, chess.engine.Limit(time=0.1))
            #sleep some time to give the illusion of playing a human opponent
            time.sleep(.5)
            print('CPU move: ', end='')
            print(CPUMove.move)
            #push the move to the board, .move just converts into a push() readable format
            board.push(CPUMove.move)
            #print the board again so the player can see the CPU's move
            print(board)
            print('')
            #create a new flag for legal moves
            isLegalMove = False
            #while we have yet to receive a legal move, and the player has not resigned,
            while(isLegalMove == False and resignFlag == False):
                #take some user input
                print('Your move: ', end='')
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
                else:
                    print('Illegal move!')
        engine.quit()        