blank = 0

pawn = 1

knight = 2

bishop = 3

rook = 4

queen = 5

king = 6

black = 8

white = 16


def pawnPromotion(pieceMoving, movePosition):
    if (pieceMoving == 17 and movePosition > 55) or (pieceMoving == 9 and movePosition < 8):
        return True
    else:
        return False