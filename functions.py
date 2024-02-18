import pieces as pieces
import copy
from collections import namedtuple

Move = namedtuple('Move', ['startPosition', 'movePosition'])

def PieceSight(piece, loc, board, potential = False):
    match piece:
        case (10 | 18):#Knights
            moves = knightSight(piece, loc, board)

        case (12 | 20):#Rooks
            moves = rookSight(piece, loc, board, potential)

        case (11 | 19):#Bishops
            moves = bishopSight(piece, loc, board, potential)

        case (9 | 17): #Pawns
            moves = pawnSight(piece, loc, board, potential)

        case (13 | 21):#Queens
            #Rook check half
            moves = rookSight(piece, loc, board, potential)
            #Bishop Check Half
            moves += bishopSight(piece, loc, board, potential)

        case (14 | 22):#Kings
            moves = kingSight(piece, loc, board)
        
        case _:
            moves = []

    return moves

def validMoves(piece, loc, board, pins, potentialSight):
    possibleMoves = PieceSight(piece, loc, board)

    if piece == 14 or piece == 22:
        return [move for move in possibleMoves if move.movePosition not in potentialSight]


    pinsCopy = copy.deepcopy(pins)
    for attack in pinsCopy:
        if len(attack) == 1:
            #Must take if attacking piece next to king
            possibleMoves = [move for move in possibleMoves if move.movePosition in attack]
        elif loc  in attack:
            attack.remove(loc)
            save = attack.pop(0)
            if all(board[piece] == 0 for piece in attack):
                attack.insert(0, save)
                possibleMoves = [move for move in possibleMoves if move.movePosition in attack]
        else:
            save = attack.pop(0)
            if all(board[piece] == 0 for piece in attack):
                attack.insert(0, save)
                possibleMoves = [move for move in possibleMoves if move.movePosition in attack] 

    return possibleMoves

def colorSight(board, color):
    ultraVision = list()

    if color == 8:
        pins = findPins(board, 16)
        potentialSight = possibleAttacksOnKing(board, 16)
    else:
        pins = findPins(board, 8)
        potentialSight = possibleAttacksOnKing(board, 8)
    
    for i, square in enumerate(board):
        if (square > 0 and square < 16 and color == 8) or (square > 16 and color == 16):
            pieceVision = validMoves(square, i, board, pins, potentialSight)

            if pieceVision:
                ultraVision += pieceVision

    return ultraVision

def potentialSight(board, color):
    ultraVision = list()

    for i, square in enumerate(board):
        if (square > 0 and square < 16 and color == 8) or (square > 16 and color == 16):
            pieceVision = PieceSight(square, i, board)

            if pieceVision:
                ultraVision += pieceVision

    return ultraVision

def possibleAttacksOnKing(board, color):
    ultraVision = list()

    for i, square in enumerate(board):
        if (square > 0 and square < 16 and color == 8) or (square > 16 and color == 16):
            pieceVision = PieceSight(square, i, board, True)

            pieceVision = [move.movePosition for move in pieceVision]

            if pieceVision:
                ultraVision += pieceVision

    return ultraVision

def IsInCheck(king, board):
    check = False
    #Checking the location of the king for board vision
    if king < 16:
        pieceSights = potentialSight(board, 16)
        for move in pieceSights:
            if board[move.movePosition] == 14:
                check = True
    if king > 16:
        pieceSights = potentialSight(board, 8)
        for move in pieceSights:
                if board[move.movePosition] == 22:
                    check = True

    return check

def IsInCheckmate(color, board):
    possibleMoves = colorSight(board, color)

    return not possibleMoves

def gameOver(board):
    if IsInCheckmate(8, board) or IsInCheckmate(16, board):
        return True
    else:
        return False
    
def utility(board):
    if IsInCheckmate(8, board):
        return 998
    elif IsInCheckmate(16, board):
        return -998
    else:
        return 0

#########################
##Individual Piece Sights
def knightSight(piece, loc, board):
    moves = []

    if loc % 8 > 1:
        if loc > 7:
            moves.append(Move(loc, loc - 10))
        if loc < 56:
            moves.append(Move(loc, loc + 6))
    if loc % 8 < 6:
        if loc > 7:
            moves.append(Move(loc, loc - 6))
        if loc < 56:
            moves.append(Move(loc, loc + 10))
    if loc > 15:
        if loc % 8 > 0:
            moves.append(Move(loc, loc - 17))
        if loc % 8 < 7:
            moves.append(Move(loc, loc - 15))
    if loc < 48:
        if loc % 8 > 0:
            moves.append(Move(loc, loc + 15))
        if loc % 8 < 7:
            moves.append(Move(loc, loc + 17))

    movesCopy =  moves.copy()
                
    for move in movesCopy:
        if piece == 10 and board[move.movePosition] < 16 and board[move.movePosition] > 0:
            moves.remove(move)
                
        if piece == 18 and board[move.movePosition] > 16:
            moves.remove(move) 

    return moves               

def rookSight(piece, loc, board, potential = False):
    moves = []
    directions = (1, -1, 8, -8)
    distances = distanceToEdge('r', loc)

    for i, movement in enumerate(directions):
        check = loc + movement

        while distances[i] > 0:
            if board[check] == 0:
                moves.append(Move(loc, check))
                check += movement
                distances[i] -= 1
            elif (piece < 16 and board[check] > 16) or (piece > 16 and board[check] < 16) or potential:
                moves.append(Move(loc, check))
                distances[i] = 0
            else:
                distances[i] = 0

    return moves

def bishopSight(piece, loc, board, potential = False):
    moves = []
    directions = (7, 9, -7, -9)
    distances = distanceToEdge('b', loc)

    for i, movement in enumerate(directions):
        check = loc + movement

        while distances[i] > 0:
            if board[check] == 0:
                moves.append(Move(loc, check))
                check += movement
                distances[i] -= 1
            elif (piece < 16 and board[check] > 16) or (piece > 16 and board[check] < 16) or potential:
                moves.append(Move(loc, check))
                distances[i] = 0
            else:
                distances[i] = 0

    return moves

def pawnSight(piece, loc, board, potential = False):
    moves = []

    if (piece == 9): #Black Pawn
        if loc > 7 and board[loc - 8] == 0 and not potential:
            moves.append(Move(loc, loc - 8))
            if (loc > 47 and board[loc - 16] == 0):
                moves.append(Move(loc, loc - 16))

        if (loc > 7 and loc % 8 !=7 and board[loc - 7] > 16):
            moves.append(Move(loc, loc - 7))
        if (loc > 7 and loc % 8 != 0 and board[loc - 9] > 16):
            moves.append(Move(loc, loc - 9))

    else: #White Pawn
        if loc < 56 and board[loc + 8] == 0 and not potential:
            moves.append(Move(loc, loc + 8))
            if (loc < 16 and board[loc + 16] == 0):
                moves.append(Move(loc, loc + 16))

        if (loc < 56 and loc % 8 != 0 and 0 < board[loc + 7] < 16):
            moves.append(Move(loc, loc + 7))
        if (loc < 56 and loc % 8 != 7 and 0 < board[loc + 9] < 16):
            moves.append(Move(loc, loc + 9))

    return moves

def kingSight(piece, loc, board):
    moves = []

    for i in range (-1, 2):
        for g in range (-1, 2):
            check = (loc + g + 8*i)
            if (loc % 8 != 0 or g > -1) and (loc % 8 != 7 or g < 1):
                if check <= 63 and check >= 0 and (i!=0 or g!=0):
                    if board[check] == 0 or (piece == 14 and board[check] > 16) or (piece == 22 and board[check] < 16):
                        moves.append(Move(loc, check))

    return moves
############################

def rookPins(piece, loc, board):
    moveLocs = []
    directions = (1, -1, 8, -8)
    distances = distanceToEdge('r', loc)

    for i, movement in enumerate(directions):
        movesSet = [loc]
        check = loc + movement

        while distances[i] > 0:
            attackingOpposite = (22 > board[check] > 16 and piece < 16) or (board[check] < 14 and piece > 16)

            if board[check] == 0 or attackingOpposite:
                movesSet.append(check)
                check += movement
                distances[i] -= 1
            elif (board[check] == 14 and piece > 16) or (board[check] == 22 and piece < 16):
                moveLocs.append(movesSet)
                distances[i] = 0
            else:
                distances[i] = 0
            
    return moveLocs

def bishopPins(piece, loc, board):
    moveLocs = []
    directions = (7, 9, -7, -9)
    distances = distanceToEdge('b', loc)

    for i, movement in enumerate(directions):
        movesSet = [loc]
        check = loc + movement

        while distances[i] > 0:
            attackingOpposite = (22 > board[check] > 16 and piece < 16) or (board[check] < 14 and piece > 16)
            
            if board[check] == 0 or attackingOpposite:
                movesSet.append(check)
                check += movement
                distances[i] -= 1
            elif (board[check] == 14 and piece > 16) or (board[check] == 22 and piece < 16):
                moveLocs.append(movesSet)
                distances[i] = 0
            else:
                distances[i] = 0

    return moveLocs

def findPins(board, color):
    pins = list()

    if color == 8:
        for i, square in enumerate(board):
            if square == 11 or square == 13:
                pins += bishopPins(square, i, board)
            if square == 12 or square == 13:
                pins += rookPins(square, i, board)
    else:
        for i, square in enumerate(board):
            if square == 19 or square == 21:
                pins += bishopPins(square, i, board)
            if square == 20 or square == 21:
                pins += rookPins(square, i, board)

    return pins

#Piece is r for rook or b for bishop
def distanceToEdge(piece, location):
    right = 7 - location % 8
    left = location % 8
    up = 7 - int(location/8)
    down = int(location/8)

    if piece == 'r':
        distances = [right, left, up, down]
    elif piece == 'b':
        distances = [min(up, left), min(up, right), min(down, right), min(down, left)]

    return distances    