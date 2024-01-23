import functions as funcs
import random as rand
import boardFunctions
from icecream import ic

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

    def towardsMiddle(move):
        distance = move.movePosition % 8 - 3.5
        distance2 = move.startPosition % 8 - 3.5

        if abs(distance) < abs(distance2) or abs(distance) < 2.5:
            return True
        else:
            return False
            
        
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
    

    def calculateFavorability(move, board, phase, color):
        favorability = 0

        '''if parameters.allowsTake(move, board, color) == True:
            newBoard = board[::]
            newBoard[move.startPosition] = 0
            newBoard[move.movePosition] = 0

            if move.pieceTaken != 0:
                value = parameters.goodTrade(move)
                value = value*parameters.goodTradeValue[phase]
                favorability += value
            elif move.movePosition in funcs.allFuncs.potentialSight(newBoard, color):
                True
            else:
                value = parameters.calculatePieceValue(move.pieceMoving)
                value = value*parameters.allowsTakeValue[phase]
                favorability += value
        elif move.pieceTaken != 0:
            value = parameters.calculatePieceValue(move.pieceTaken)
            value = value*parameters.undefendedTakeValue[phase]
            favorability += value'''

        '''for i, piece in enumerate(board):
            if 0 < piece - color < 8:
                newMove = funcs.move(i, i, piece, piece, False, color)
                if parameters.allowsTake(newMove, board, color) == True:
                    newBoard = board[::]
                    newBoard[newMove.movePosition] = 0
                    if newMove.movePosition in funcs.allFuncs.potentialSight(board, color):
                 
                        value = parameters.goodTrade(move)
                        value = value*parameters.goodTradeValue[phase]
                        favorability += value
                    else:
                        value = parameters.calculatePieceValue(move.pieceMoving)
                        value = value*parameters.allowsTakeValue[phase]
                        favorability += value'''


        if favorability > 0 and parameters.putsInCheck(move, board) == True:
            favorability += parameters.putsInCheckValue[phase]

        if parameters.towardsMiddle(move) == True:
            favorability += parameters.towardsMiddleValue[phase]

        #if parameters.defended(move, board) == True:
         #   favorability += parameters.defendedValue[phase]

        if parameters.kingMove(move) == True:
            favorability += parameters.kingMoveValue[phase]

        if parameters.pawnPush(move) == True:
            favorability += parameters.pawnPushValue[phase]

        if parameters.pawnPromotion(move) == True:
            favorability += parameters.pawnPromotionValue[phase]

        if parameters.putsInCheckmate(move, board) == True:
            favorability += parameters.putsInCheckMateValue[phase]

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
    color= int
    if turn % 2 == 0:
        color = 8
    else:
        color = 16

    phase = 0
    if turn > 6:
        phase = 1
    if turn > 15:
        phase = 2

    validMoves = set()

    for i, square in enumerate(board):
        if 0 < square < 16:
            moves = funcs.allFuncs.validMoves(square, i, board)
        else:
            moves = set()
        validMoves = validMoves | moves


    best = 0
    bestMove = set()
    bestMove.add(funcs.move())

    #if depth + 1 == maxDepth:
    for move in validMoves:
        score = parameters.calculateFavorability(move, board, phase, color)
        #score = score*rand.randrange(8, 11)
        if score > best:
            best = score
            bestMove = {move}
        elif score == best:
            bestMove.add(move)

    """else:
        if color == 8:
            bestEval = 500
        if color == 16:
            bestEval = -500
        for move in validMoves:
            AIMoves(board, move)
            eval = AIMove(board, turn+1, depth+1, maxDepth)
            board[move.startPosition] = move.pieceMoving
            board[move.movePosition] = move.pieceTaken

            if (color == 8 and eval < bestEval) or (color == 16 and eval > bestEval):
                bestEval = eval
                bestMove = [move]
            elif eval == bestEval:
                bestMove.append(move)

        bestMove = rand.choice(bestMove)"""
    
    bestMove = rand.sample(tuple(bestMove), 1)
    bestMove = bestMove[0]
    good = parameters.calculateFavorability(bestMove, board, phase, color)
    
    AIMoves(board, bestMove)

    if depth > 0:
        eval = simpleEvaluation(board)
        board[bestMove.startPosition] = bestMove.pieceMoving
        board[bestMove.movePosition] = bestMove.pieceTaken
        return eval


def AIMoves(board, moveToMake):
    if funcs.allFuncs.pawnPromotion(moveToMake) == True:
        board[moveToMake.movePosition] = moveToMake.pieceMoving + 4
    else:
        board[moveToMake.movePosition] = moveToMake.pieceMoving
    board[moveToMake.startPosition] = 0