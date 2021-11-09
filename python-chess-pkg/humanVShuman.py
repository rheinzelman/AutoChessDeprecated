'''
make move = user input
if move is legal, push()
if not, ask for more input

'''

import chess
import chess.svg

board = chess.Board()


while(board.legal_moves.count() > 0):
    isLegalMove = False
    while(isLegalMove == False):
        move = chess.Move.from_uci(input())
        if(move in board.legal_moves):
            isLegalMove = True
    board.push(move)
    print(board)