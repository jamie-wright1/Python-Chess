import pieces as pieces
from icecream import ic
from collections import namedtuple

Move = namedtuple('Move', ['startPosition', 'movePosition'])


class allFuncs:

    def __init__(self):
        pass

    @staticmethod
    def pawnPromotion(move):
        if move.pieceMoving == 17 and move.movePosition > 55:
            return True
        elif move.pieceMoving == 9 and move.movePosition < 8:
            return True
        else:
            return False

    @staticmethod
    def pieceSwap(newPiece, loc, board):
        board[loc] = newPiece
        return board

    @staticmethod
    def PieceSight(piece, loc, board):
        check = loc
        moves = list()

        match piece:
            case (10 | 18):#Knights
                #Maybe fix?
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

            case (12 | 20):#Rooks
                directions = (1, -1, 8, -8)

                for movement in directions:
                    check = loc
                    check += movement
                    
                    while (0 <= check <= 63 and board[check] == 0):
                        if (movement == -1 and check % 8 == 7) or (movement == 1 and check % 8 == 0):
                            check = 64
                        else:
                            moves.append(Move(loc, check))
                            check += movement

                    #To fix
                    if 0 <= check <= 63 and ((movement == -1 and check % 8 != 7) or (movement == 1 and check % 8 != 0) or (movement == 8 or movement == -8)):
                        if (piece == 12 and board[check] > 16) or (piece == 20 and board[check] < 16):
                            moves.append(Move(loc, check))

            case (11 | 19):#Bishops
                directions = (7, -7, 9, -9)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if ((movement == -9 or movement == 7) and check % 8 == 7) or ((movement == -7 or movement == 9) and check % 8 == 0):
                            check = 64
                        else:
                            moves.append(Move(loc, check))
                            check += movement

                    if (0 <= check <= 63) and (((movement == 9 or movement == -7) and check % 8 != 0) or (movement !=9 and movement != -7)) and (((movement == 7 or movement == -9) and check % 8 != 7) or (movement != 7 and movement !=-9)):
                        if (piece == 11 and board[check] > 16) or (piece == 19 and board[check] < 16):
                           moves.append(Move(loc, check))

            case (9):#Black Pawn
                if loc > 7 and board[loc - 8] == 0:
                    moves.append(Move(loc, loc - 8))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    if (loc > 47 and board[loc - 16] == 0):
                        moves.append(Move(loc, loc - 16))
   
                if (loc > 7 and loc % 8 !=7 and board[loc - 7] > 16):
                    moves.append(Move(loc, loc - 7))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                if (loc > 7 and loc % 8 != 0 and board[loc - 9] > 16):
                    moves.append(Move(loc, loc - 9))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)

            case (17):#White pawn
                if loc < 56 and board[loc + 8] == 0:
                    moves.append(Move(loc, loc + 8))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    if (loc < 16 and board[loc + 16] == 0):
                        moves.append(Move(loc, loc + 16))

                if (loc < 56 and loc % 8 != 0 and 0 < board[loc + 7] < 16):
                    moves.append(Move(loc, loc + 7))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                if (loc < 56 and loc % 8 != 7 and 0 < board[loc + 9] < 16):
                    moves.append(Move(loc, loc + 9))
                    #moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)

            case (13 | 21):#Queens
                #Rook check half
                directions = (1, -1, 8, -8)

                for movement in directions:
                    check = loc
                    check += movement
                    
                    while (0 <= check <= 63 and board[check] == 0):
                        if (movement == -1 and check % 8 == 7) or (movement == 1 and check % 8 == 0):
                            check = 64
                        else:
                            moves.append(Move(loc, check))
                            check += movement

                    #To fix
                    if 0 <= check <= 63 and ((movement == -1 and check % 8 != 7) or (movement == 1 and check % 8 != 0) or (movement == 8 or movement == -8)):
                        if (piece == 13 and board[check] > 16) or (piece == 21 and board[check] < 16):
                            moves.append(Move(loc, check))

                #Bishop Check Half
                directions = (7, -7, 9, -9)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if ((movement == -9 or movement == 7) and check % 8 == 7) or ((movement == -7 or movement == 9) and check % 8 == 0):
                            check = 64
                        else:
                            moves.append(Move(loc, check))
                            check += movement

                    if (0 <= check <= 63) and (((movement == 9 or movement == -7) and check % 8 != 0) or (movement !=9 and movement != -7)) and (((movement == 7 or movement == -9) and check % 8 != 7) or (movement != 7 and movement !=-9)):
                        if (piece == 13 and board[check] > 16) or (piece == 21 and board[check] < 16):
                           moves.append(Move(loc, check))

            case (14 | 22):#Kings
                for i in range (-1, 2):
                    for g in range (-1, 2):
                        check = (loc + g + 8*i)
                        if (loc % 8 != 0 or g > -1) and (loc % 8 != 7 or g < 1):
                            if check <= 63 and check >= 0 and (i!=0 or g!=0):
                                if board[check] == 0 or (piece == 14 and board[check] > 16) or (piece == 22 and board[check] < 16):
                                    moves.append(Move(loc, check))
           
            case _:
                moves = list()

        return moves

    @staticmethod
    def validMoves(piece, loc, board):
        possibleMoves = allFuncs.PieceSight(piece, loc, board)
       
        movesCopy = possibleMoves.copy()

        for move in movesCopy:
            boardToCheck = board[::]
            boardToCheck[move.movePosition] = piece
            boardToCheck[loc] = 0
            
            if  allFuncs.IsInCheck(piece, boardToCheck) == True:
                moveCopy = move
                possibleMoves.remove(moveCopy)

        return possibleMoves
    
    @staticmethod
    def colorSight(board, color):
        ultraVision = list()
        
        for i, square in enumerate(board):
            if (((square > 0 and square < 16 and color == 8) or (square > 16 and color == 16))):
                pieceVision = (allFuncs.validMoves(square, i, board))

                if pieceVision:
                    ultraVision += pieceVision

        return ultraVision

    @staticmethod
    def potentialSight(board, color):
        ultraVision = list()

        for i, square in enumerate(board):
            if (((square > 0 and square < 16 and color == 8) or (square > 16 and color == 16))):
                pieceVision = (allFuncs.PieceSight(square, i, board))

                if pieceVision:
                    ultraVision += pieceVision

        return ultraVision
    
    @staticmethod
    def IsInCheck(king, board):
        check = False
        #Checking the location of the king for board vision
        if king < 16:
            pieceSights = allFuncs.potentialSight(board, 16)
            for move in pieceSights:
                if board[move.movePosition] == 14:
                    check = True
        if king > 16:
            pieceSights = allFuncs.potentialSight(board, 8)
            for move in pieceSights:
                    if board[move.movePosition] == 22:
                        check = True

        return check
    
    @staticmethod
    def IsInCheckmate(color, board):
        possibleMoves = allFuncs.colorSight(board, color)

        return not possibleMoves
    
    @staticmethod
    def gameOver(board):
        if allFuncs.IsInCheckmate(8, board) or allFuncs.IsInCheckmate(16, board):
            return True
        else:
            return False
        
    @staticmethod
    def utility(board):
        if allFuncs.IsInCheckmate(8, board):
            return 1000
        elif allFuncs.IsInCheckmate(16, board):
            return -1000
        else:
            return 0