import pytest
import chess
import chess.engine
from ioDriver import IODriver
from gameEngine import chessEngine

# unit tests


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




if __name__ == '__main__':
    test_assignToArray()
