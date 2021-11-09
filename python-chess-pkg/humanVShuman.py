#the main chess library for move validation and gamestate checking
import chess

#initialize a new Board state called board
board = chess.Board()

#let the player choose which side they would like to play
print("Rock paper scissors to see who will play as white")

#keep track if the player has resigned
resignFlag = False

whiteTurn = True

while(board.is_game_over() == False and resignFlag == False):
    print(board)
    print('')

    #create a new flag for legal moves
    isLegalMove = False
    #while we have yet to receive a legal move, and the player has not resigned,
    while(isLegalMove == False and resignFlag == False):
        #take some user input
        if(whiteTurn):
            print('White\'s move: ', end='')
        else:
            print('Black\'s move: ', end='')
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
            whiteTurn = not whiteTurn
        else:
            print('Illegal move!')