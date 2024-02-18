import functions as funcs
import random
import boardFunctions
from icecream import ic
import time

class parameters:
    def towardsMiddle(board):
        favorability = 0

        for square in board:
            if square & 8 > 2 and square & 8 < 6:
                if square > 16:
                    favorability += 5
                elif square > 0:
                    favorability -= 5

        return favorability
            
    def calculatePieceValue(piece):
        match piece:
            case 9 | 17:
                return 1
            case 10 | 18 | 11 | 19 :
                return 3
            case 12 | 20:
                return 5
            case 13 | 21:
                return 9
            case _:
                return 0

    
    def kingStayPut(board):
        for i, square in enumerate(board):
            if square == 14:
                if i > 15:
                    return 3
            elif square == 22:
                if i < 48:
                    return -3
                
        return 0

    def pawnsAdvanced(board):
        favorability = 0

        for i, square in enumerate(board):
            if square == 9:
                favorability -= int(i/8)
            elif square == 17:
                favorability += int((7 - i/8))

        return favorability

    def checks(board):
        favorability = 0

        if funcs.IsInCheck(8, board) == True:
            favorability += 20

        if funcs.IsInCheck(16, board) == True:
            favorability -= 20

        return favorability
    
    def calculateFavorability(board):
        favorability = 0

        favorability+= 10*simpleEvaluation(board)
        favorability+= parameters.towardsMiddle(board)
        favorability+= parameters.kingStayPut(board)
        favorability+= parameters.pawnsAdvanced(board)
        favorability+= parameters.checks(board)

        if funcs.IsInCheck(8, board) == True:
            favorability += 20

        if funcs.IsInCheck(16, board) == True:
            favorability -= 20

        return favorability*random.randrange(7, 10)

#Adds up the value of every piece on the board
def simpleEvaluation(board):
    whiteValue = blackValue = 0

    for square in board:
        if square > 16:
            whiteValue += parameters.calculatePieceValue(square)
        elif square > 0:
            blackValue += parameters.calculatePieceValue(square)

    totalEval = whiteValue - blackValue

    return totalEval

def AIMove(board, turn, depth):
    begin = time.time()

    if turn % 2 == 0:
        color = 8
    else:
        color = 16

    phase = 0
    if turn > 6:
        phase = 1
    if turn > 15:
        phase = 2

    validMoves = list()

    validMoves = funcs.colorSight(board, color)

    
    bestMove = minimax(board, validMoves, depth)

    boardFunctions.boardFuncs.updateBoard(bestMove, board)

    end = time.time()
    print(end-begin)

def minimax(board, possibleMoves, depth):
    bestMove = None
    alpha, beta = -999, 999

    possibleMoves = funcs.colorSight(board, 8)
    newOrder = moveOrdering(board, possibleMoves)
    
    
    for move in newOrder:
        savePiece = boardFunctions.boardFuncs.updateBoard(move, board)
        v = max(board, alpha, beta, depth-1)
        boardFunctions.boardFuncs.undoMove(move, board, savePiece)

        if v <= alpha:
            return move
        
        if v < beta:
            beta = v
            bestMove = move

    return bestMove

def max(board, alpha, beta, depth):
    if funcs.gameOver(board) == True:
        return funcs.utility(board)
    
    if depth == 0:
        return parameters.calculateFavorability(board)

    possibleMoves = funcs.colorSight(board, 16)
    newOrder = moveOrdering(board, possibleMoves)
    
    for move in newOrder:
        savePiece = boardFunctions.boardFuncs.updateBoard(move, board)
        v = min(board, alpha, beta, depth-1)
        boardFunctions.boardFuncs.undoMove(move, board, savePiece)

        if v >= beta:
            return v
        
        if v > alpha:
            alpha = v

    return alpha

def min(board, alpha, beta, depth):
    if funcs.gameOver(board) == True:
        return funcs.utility(board)
    

    if depth == 0:
        return parameters.calculateFavorability(board)

        
    possibleMoves = funcs.colorSight(board, 8)
    newOrder = moveOrdering(board, possibleMoves)

    for move in newOrder:
        savePiece = boardFunctions.boardFuncs.updateBoard(move, board)
        v = max(board, alpha, beta, depth-1)
        boardFunctions.boardFuncs.undoMove(move, board, savePiece)

        if v <= alpha:
            return v
        
        if v < beta:
            beta = v

    return beta

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