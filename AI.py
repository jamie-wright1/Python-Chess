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
        value = int
        match piece:
            case 9 | 17:
                value = 1
            case 10 | 18 :
                value = 3
            case 11 | 19:
                value = 3
            case 12 | 20:
                value = 5
            case 13 | 21:
                value = 9
            case _:
                value = 0

        return value
    
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
                favorability -= (i / 8)/2
            elif square == 17:
                favorability += (7 - i / 8)/2

        return favorability

    def calculateFavorability(board):
        favorability = 0

        favorability+= 10*simpleEvaluation(board)
        favorability+= parameters.towardsMiddle(board)
        favorability+= parameters.kingStayPut(board)
        favorability+= parameters.pawnsAdvanced(board)

        if funcs.allFuncs.IsInCheck(8, board) == True:
            favorability += 20

        if funcs.allFuncs.IsInCheck(16, board) == True:
            favorability -= 20

        return favorability

def simpleEvaluation(board):
    whiteValue = blackValue = 0

    for square in board:
        if square > 16:
            whiteValue += parameters.calculatePieceValue(square)
        elif square > 0:
            blackValue += parameters.calculatePieceValue(square)

    totalEval = whiteValue - blackValue

    return totalEval

def AIMove(board, turn, depth, maxDepth):
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

    for i, square in enumerate(board):
        if 0 < square < 16:
            moves = funcs.allFuncs.validMoves(square, i, board)
            validMoves += moves


    bestMove = minimax(board, validMoves, maxDepth)

    executeAIMove(board, bestMove)

    end = time.time()
    print (end - begin)

def executeAIMove(board, moveToMake):
    #if funcs.allFuncs.pawnPromotion(moveToMake) == True:
        #should only have one element
        #for move in moveToMake.moveInfos:
         #   board[move[0]] = moveToMake.pieceMoving + 4
    #else:
    board[moveToMake.movePosition] = board[moveToMake.startPosition]
    board[moveToMake.startPosition] = 0

def minimax(board, possibleMoves, depth):
    bestMove = None
    alpha, beta = -99, 99

    possibleMoves = funcs.allFuncs.colorSight(board, 8)
    newOrder = moveOrdering(board, possibleMoves, 16)
    
    
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
    if funcs.allFuncs.gameOver(board) == True:
        return funcs.allFuncs.utility(board)
    
    if depth == 0:
        return parameters.calculateFavorability(board)

    possibleMoves = funcs.allFuncs.colorSight(board, 16)
    newOrder = moveOrdering(board, possibleMoves, 8)
    
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
    if funcs.allFuncs.gameOver(board) == True:
        return funcs.allFuncs.utility(board)
    

    if depth == 0:
        return parameters.calculateFavorability(board)

        
    possibleMoves = funcs.allFuncs.colorSight(board, 8)
    newOrder = moveOrdering(board, possibleMoves, 16)

    for move in newOrder:
        savePiece = boardFunctions.boardFuncs.updateBoard(move, board)
        v = max(board, alpha, beta, depth-1)
        boardFunctions.boardFuncs.undoMove(move, board, savePiece)

        if v <= alpha:
            return v
        
        if v < beta:
            beta = v

    return beta

def moveOrdering(board, possibleMoves, color):
    newList = []

    for i in range(6, 0, -1):
        for move in possibleMoves:
                if board[move.movePosition] == (i + color):
                    newList.append(move)

    for move in possibleMoves:
        if board[move.movePosition] == 0:
            newList.append(move)
    
    return newList