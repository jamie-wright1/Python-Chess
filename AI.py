import functions as funcs
import random as rand
import boardFunctions
from icecream import ic
import time

class parameters:
    
    #Temporary until depth
    def allowsTake(move, board, color):
        newBoard = board[::]
        newBoard = boardFunctions.boardFuncs.updateBoard(move, newBoard)
        if color == 8:
            attacked = funcs.allFuncs.potentialSight(newBoard, 16)
        else:
            attacked = funcs.allFuncs.potentialSight(newBoard, 8)

        for moveInfo in attacked:
            if move.movePosition == moveInfo.movePosition:
                return True
       
        return False
    
    allowsTakeValue = (-4, -4, -4)

    def goodTrade(move):
        value = parameters.calculatePieceValue(move.pieceTaken) - parameters.calculatePieceValue(move.pieceMoving)
        return value
    

    goodTradeValue = (3, 3, 3)

    def towardsMiddle(board):
        favorability = 0

        for square in board:
            if square & 8 > 2 and square & 8 < 6:
                if square > 16:
                    favorability += 5
                elif square > 0:
                    favorability -= 5

        return favorability
            
        
    towardsMiddleValue = (4, 4, 3)

    undefendedTakeValue = (4, 4, 4)

    def defended(move, board, color):
        newBoard = board[::]
        newBoard = boardFunctions.boardFuncs.updateBoard(move, newBoard)
        newBoard[move.movePosition] = 0

        if color == 8:
            defended = funcs.allFuncs.potentialSight(newBoard, 8)
        else:
            defended = funcs.allFuncs.potentialSight(newBoard, 16)

        for moveInfo in defended:
            if move.movePosition == moveInfo.movePosition:
                return True
       
        return False


    defendedValue = (10, 10, 10)

    def kingMove(move):
        return move.pieceMoving == 14 or move.pieceMoving == 22

    kingMoveValue = (-3, -3, 0)

    def pawnPush(move):
        return move.pieceMoving == 9 or move.pieceMoving == 17

    pawnPushValue = (2, 2, 0)

    def pawnPromotion(move):
        return (move.movePosition < 8 and move.pieceMoving == 9) or (move.movePosition > 55 and move.pieceMoving == 17)

    pawnPromotionValue = (80, 80, 80)

    def putsInCheck(move, board):
        newBoard = board[::]
        newBoard = boardFunctions.boardFuncs.updateBoard(move, newBoard)

        return funcs.allFuncs.IsInCheck(move.pieceMoving, newBoard)


    putsInCheckValue = (5, 10, 15)

    def putsInCheckmate(move, board):
        True

    putsInCheckMateValue = (1000, 1000, 1000)
    
    castleValue = (30, 15, 10)

    phases = int

    isTradeValue = (10, 15, 20)

    isWinning = (True, False)

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

        favorability+= simpleEvaluation(board)
        favorability+= parameters.towardsMiddle(board)
        favorability+= parameters.kingStayPut(board)
        favorability+= parameters.pawnsAdvanced(board)

        if funcs.allFuncs.IsInCheck(8, board) == True:
            favorability += 20

        if funcs.allFuncs.IsInCheck(16, board) == True:
            favorability -= 20

        #if parameters.defended(move, board) == True:
         #   favorability += parameters.defendedValue[phase]

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
    board[moveToMake.movePosition] = board[moveToMake.starPosition]
    board[moveToMake.startPosition] = 0

def minimax(board, possibleMoves, maxDepth):
    moveToPlay = tuple()
    best = 99

    possibleMoves = funcs.allFuncs.colorSight(board, 8)
    ic(possibleMoves)
    newOrder = moveOrdering(board, possibleMoves, 16)
    ic(newOrder)
    
    
    for move in possibleMoves:
        boardCopy = board[::]
        boardCopy = boardFunctions.boardFuncs.updateBoard(move, board[move.startPosition], move.startPosition, boardCopy)

        v = max(boardCopy, best, 0, maxDepth)

        if v < best:
            best = v
            moveToPlay = move

    return moveToPlay

def max(board, prune, depth, maxDepth):
    if funcs.allFuncs.gameOver(board) == True:
        return funcs.allFuncs.utility(board)
    
    if depth == maxDepth:
        return parameters.calculateFavorability(board)
    
    best = -99

    possibleMoves = funcs.allFuncs.colorSight(board, 16)
    
    for move in possibleMoves:
        boardCopy = board[::]
        boardCopy = boardFunctions.boardFuncs.updateBoard(move, board[move.startPosition], move.startPosition, boardCopy)

        v = min(boardCopy, best, depth+1, maxDepth)

        if v >= prune:
            return v
        
        if v > best:
            best = v
        
    return best

def min(board, prune, depth, maxDepth):
    if funcs.allFuncs.gameOver(board) == True:
        return funcs.allFuncs.utility(board)
    

    if depth == maxDepth:
        return parameters.calculateFavorability(board)

    best = 99
        
    possibleMoves = funcs.allFuncs.colorSight(board, 8)


    for move in possibleMoves:

        boardCopy = board[::]
        boardCopy = boardFunctions.boardFuncs.updateBoard(move, board[move.startPosition], move.startPosition, boardCopy)

        v = max(boardCopy, best, depth+1, maxDepth)

        if v <= prune:
            return v
        
        if v < best:
            best = v

    return best

def moveOrdering(board, possibleMoves, color):
    newList = []

    for i in range(6, 0, -1):
        for move in possibleMoves:
                if board[move.movePosition] == (i + color):
                    ic("Appended")
                    newList.append(move)

    for move in possibleMoves:
        if board[move.movePosition] == 0:
            newList.append(move)
    
    return newList