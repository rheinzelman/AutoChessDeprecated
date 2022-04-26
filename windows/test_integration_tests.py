import pytest
import chess
import chess.engine
from ioDriver import IODriver
from gameEngine import chessEngine

iterations = 4

# integration test of formatASCII and assignToArray with the chess library's board call
def test_formatASCII():
    i = IODriver()
    g1 = chessEngine('W', '0', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    boardArray1 = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    assert i.formatASCII(g1.board) == boardArray1
    g1.quitEngine()
    g2 = chessEngine('W', '0', 'RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr')
    boardArray2 = [
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
    ]
    assert i.formatASCII(g2.board) == boardArray2
    g2.quitEngine()
    g3 = chessEngine('W', '0', '8/8/8/8/8/8/8/8')
    boardArray3 = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    assert i.formatASCII(g3.board) == boardArray3
    g3.quitEngine()

def test_pushCPUMove():
    game2 = chessEngine('W', '1', '')
    auxGame = chessEngine('B', '1', '')

    for i in range(0, iterations):
        assert game2.pushPlayerMove(str(auxGame.pushCPUMove())) == True
        assert auxGame.pushPlayerMove(str(game2.pushCPUMove())) == True
    print()
    print("test push CPU move board")
    print(game2.board)
    game2.quitEngine()
    auxGame.quitEngine()

if __name__ == '__main__':
    test_integration_tests()