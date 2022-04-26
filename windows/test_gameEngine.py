import pytest
import chess
import chess.engine
from ioDriver import IODriver
from gameEngine import chessEngine

iterations = 4

# unit test
def test_pushPlayerMove():
    legal_move1 = "e2e4"
    legal_move2 = "e7e5"
    illegal_move1 = "e1c1"
    illegal_move2 = "d8c8"

    game1 = chessEngine('P', '1', '')
    assert game1.pushPlayerMove(legal_move1) == True
    assert game1.pushPlayerMove(legal_move2) == True
    assert game1.pushPlayerMove(illegal_move1) == False
    assert game1.pushPlayerMove(illegal_move2) == False

    game1.quitEngine()
    print()
    print("test push player move board")
    print(game1.board)

def test_isPawn():
    game1 = chessEngine('P', '1', '')
    assert game1.isPawn(('a',2)) == True
    assert game1.isPawn(('b',2)) == True
    assert game1.isPawn(('c',2)) == True
    assert game1.isPawn(('d',2)) == True
    assert game1.isPawn(('e',2)) == True
    assert game1.isPawn(('f',2)) == True
    assert game1.isPawn(('g',2)) == True
    assert game1.isPawn(('h',7)) == True
    assert game1.isPawn(('a',7)) == True
    assert game1.isPawn(('b',7)) == True
    assert game1.isPawn(('c',7)) == True
    assert game1.isPawn(('d',7)) == True
    assert game1.isPawn(('e',7)) == True
    assert game1.isPawn(('f',7)) == True
    assert game1.isPawn(('g',7)) == True
    assert game1.isPawn(('h',7)) == True
    game1.quitEngine()

def test_getLastMove():
    game1 = chessEngine('B', '1', '')
    auxGame = chessEngine('W', '1', '')

    for i in range(0, iterations):
        last_move1 = game1.pushCPUMove()
        assert game1.getLastMove() == str(last_move1)
        last_move2 = str(auxGame.pushCPUMove())
        game1.pushPlayerMove(last_move2)
        assert auxGame.getLastMove() == str(last_move2)


    game1.quitEngine()
    auxGame.quitEngine()

if __name__ == '__main__':
    test_assignToArray()
