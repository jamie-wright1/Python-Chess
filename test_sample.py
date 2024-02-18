
from AI import parameters
import pytest

def moveOrdering(board, possibleMoves):
    scores = [""]*len(possibleMoves)

    for i, move in enumerate(possibleMoves):
        pieceMoving, pieceTaken = board[move[0]], board[move[1]]

        if pieceTaken != 0:
            scores[i] = (parameters.calculatePieceValue(pieceTaken) - parameters.calculatePieceValue(pieceMoving))
        else:
            scores[i] = 0

    sortedMoves = [x for _, x in sorted(zip(scores, possibleMoves), reverse=True)]

    return sortedMoves

def test_move_ordering():
    testBoard = [2+8, 4+16, 2+16, 3+8, 5+8]

    testMoves = [(0, 3), (0, 1), (4, 1),]

    assert moveOrdering(testBoard, testMoves) == [(0, 1), (0, 3), (4,1)]


def test():
    attack = [0, 0, 0, 5, 0, 0, 0, 0]
    attack.pop()
    assert(all(piece == 0 for piece in attack))
    