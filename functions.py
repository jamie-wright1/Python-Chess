import pieces as pieces
from icecream import ic

class move:
    
    def __init__(self, startPosition = -1, movePosition = -1, pieceMoving = -1, pieceTaken = -1, isTake = False, colorOfMover = -1, isCastle = False, isPromotion = False):
        self.startPosition = startPosition
        self.movePosition = movePosition

        self.pieceMoving = pieceMoving

        self.pieceTaken = pieceTaken
        self.isTake = isTake
        
        self.colorOfMover = colorOfMover

        self.isCastle = isCastle

        self.isPromotion = isPromotion

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
        if piece > 16:
            color = 16
        else:
            color = 8

        vision = set()
        check = loc

        match piece:
            case (10 | 18):#Knights
                
                if loc % 8 > 1:
                    if loc > 7:
                        vision.add(move(loc, loc -10, piece, board[loc - 10], False, color))
                    if loc < 56:
                        vision.add(move(loc, loc + 6, piece, board[loc + 6], False, color))

                if loc % 8 < 6:
                    if loc > 7:
                        vision.add(move(loc, loc - 6, piece, board[loc - 6], False, color))
                    if loc < 56:
                        vision.add(move(loc, loc + 10, piece, board[loc + 10], False, color))

                if loc > 15:
                    if loc % 8 > 0:
                        vision.add(move(loc, loc - 17, piece, board[loc - 17], False, color))
                    if loc % 8 < 7:
                        vision.add(move(loc, loc - 15, piece, board[loc - 15], False, color))


                if loc < 48:
                    if loc % 8 > 0:
                        vision.add(move(loc, loc + 15, piece, board[loc + 15], False, color))
                    if loc % 8 < 7:
                        vision.add(move(loc, loc + 17, piece, board[loc + 17], False, color))

                visionCopy = vision.copy()
                
                for moveInfo in visionCopy:
                    if piece == 10 and moveInfo.pieceTaken < 16 and moveInfo.pieceTaken > 0:
                        vision.remove(moveInfo)
                        
                    if piece == 18 and moveInfo.pieceTaken > 16:
                        vision.remove(moveInfo)                

            case (12 | 20):#Rooks
                directions = (1, -1, 8, -8)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if movement == -1 and check % 8 == 7:
                            check = 64
                        elif movement == 1 and check % 8 == 0:
                            check = 64
                        else:
                            vision.add(move(loc, check, piece, 0, False, color))
                            check += movement

                    if 0 <= check <= 63 and ((movement == -1 and check % 8 != 7) or (movement == 1 and check % 8 != 0) or (movement == 8 or movement == -8)):
                        if (piece == 12 and board[check] > 16) or (piece == 20 and board[check] < 16):
                            vision.add(move(loc, check, piece, board[check], False, color))

            case (11 | 19):#Bishops
                directions = (7, -7, 9, -9)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if (movement == -9 or movement == 7) and check % 8 == 7:
                            check = 64
                        elif (movement == -7 or movement == 9) and check % 8 == 0:
                            check = 64
                        else:
                            vision.add(move(loc, check, piece, 0, False, color))
                            check += movement

                    if (0 <= check <= 63) and (((movement == 9 or movement == -7) and check % 8 != 0) or (movement !=9 and movement != -7)) and (((movement == 7 or movement == -9) and check % 8 != 7) or (movement != 7 and movement !=-9)):
                        if (piece == 11 and board[check] > 16) or (piece == 19 and board[check] < 16):
                            vision.add(move(loc, check, piece, board[check], False, color))

            case (9):#Black Pawn
             
                if board[loc - 8] == 0:
                    moveInfo = move(loc, loc - 8, piece, 0, False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)
                    if (loc > 47 and board[loc - 16] == 0):
                        vision.add(move(loc, loc - 16, piece, 0, False, color))

                if piece == 9 and oldMove.pieceMoving == 17 and oldMove.movePosition - oldMove.startPosition == 16:
                    True
   
                if (loc > 7 and loc % 8 !=7 and board[loc - 7] > 16):
                    moveInfo = move(loc, loc - 7, piece, board[loc - 7], False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)
                if (loc > 7 and loc % 8 != 0 and board[loc - 9] > 16):
                    moveInfo = move(loc, loc - 9, piece, board[loc - 9], False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)

            case (17):#White pawn
         
                if board[loc + 8] == 0:       
                    moveInfo = move(loc, loc + 8, piece, 0, False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)
                    if (loc < 16 and board[loc + 16] == 0):
                        vision.add(move(loc, loc + 16, piece, 0, False, color))

                if (loc < 56 and loc % 8 != 0 and (16 > board[loc + 7] > 0)):
                    moveInfo = move(loc, loc + 7, piece, board[loc + 7], False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)
                if (loc < 56 and loc % 8 != 7 and (0 < board[loc + 9] < 16)):
                    moveInfo = move(loc, loc + 9, piece, board[loc+9], False, color)
                    moveInfo.isPromotion = allFuncs.pawnPromotion(moveInfo)
                    vision.add(moveInfo)

            case (13 | 21):#Queens
                #Rook check half
                directions = (1, -1, 8, -8)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if movement == -1 and check % 8 == 7:
                            check = 64
                        elif movement == 1 and check % 8 == 0:
                            check = 64
                        else:
                            vision.add(move(loc, check, piece, 0, False, color))
                            check += movement

                    if 0 <= check <= 63 and ((movement == -1 and check % 8 != 7) or (movement == 1 and check % 8 != 0) or (movement == 8 or movement == -8)):
                        if (piece == 13 and board[check] > 16) or (piece == 21 and board[check] < 16):
                            vision.add(move(loc, check, piece, board[check], False, color))

                #Bishop Check Half
                directions = (7, -7, 9, -9)

                for movement in directions:
                    check = loc

                    check += movement
                    while (0 <= check <= 63 and board[check] == 0):
                        if (movement == -9 or movement == 7) and check % 8 == 7:
                            check = 64
                        elif (movement == -7 or movement == 9) and check % 8 == 0:
                            check = 64
                        else:
                            vision.add(move(loc, check, piece, 0, False, color))
                            check += movement

                    if (0 <= check <= 63) and (((movement == 9 or movement == -7) and check % 8 != 0) or (movement !=9 and movement != -7)) and (((movement == 7 or movement == -9) and check % 8 != 7) or (movement != 7 and movement !=-9)):
                        if (piece == 13 and board[check] > 16) or (piece == 21 and board[check] < 16):
                            vision.add(move(loc, check, piece, board[check], False, color))

            case (14 | 22):#Kings
                for i in range (-1, 2):
                    for g in range (-1, 2):
                        check = (loc + g + 8*i)
                        if (loc % 8 != 0 or g > -1) and (loc % 8 != 7 or g < 1):
                            if check <= 63 and check >= 0 and (i!=0 or g!=0):
                                if board[check] == 0:
                                    vision.add(move(loc, check, piece, board[check], False, color))
                                elif piece == 14 and board[check] > 16:
                                    vision.add(move(loc, check, piece, board[check], False, color))
                                elif piece == 22 and board[check] < 16:
                                    vision.add(move(loc, check, piece, board[check], False, color))
           
            case _:
                vision = set()

        return vision

    @staticmethod
    def validMoves(piece, loc, board):
        vision = allFuncs.PieceSight(piece, loc, board)
       
        newVision = vision.copy()

        for moveInfo in newVision:
            boardToCheck = board[::]
            boardToCheck[moveInfo.movePosition] = piece
            boardToCheck[moveInfo.startPosition] = 0
            
            if  allFuncs.IsInCheck(moveInfo.pieceMoving, boardToCheck) == True:
                newSquare = moveInfo
                vision.remove(newSquare)

        return vision
    
    @staticmethod
    def colorSight(board, color):
        ultraVision = set()
        
        for i, square in enumerate(board):
            pieceVision = set()
            if (((square > 0 and square < 16 and color == 8) or (square > 16 and color == 16))):
                pieceVision = allFuncs.validMoves(square, i, board)

                ultraVision = ultraVision | pieceVision

        return ultraVision

    @staticmethod
    def potentialSight(board, color):
        ultraVision = set()

        for i, square in enumerate(board):
            pieceVision = set()
            if (((square > 0 and square < 16 and color == 8) or (square > 16 and color == 16))):
                pieceVision = allFuncs.PieceSight(square, i, board)

                ultraVision = ultraVision | pieceVision

        return ultraVision
    
    @staticmethod
    def IsInCheck(king, board):
        check = False
        #Checking the location of the king for board vision
        if king < 16:
            moves = allFuncs.potentialSight(board, 16)
            for moveInfo in moves:

                if moveInfo.pieceTaken == 14:
                    check = True

        if king > 16:
            moves = allFuncs.potentialSight(board, 8)
            for moveInfo in moves:

                if moveInfo.pieceTaken == 22:
                    check = True

        return check
    
    @staticmethod
    def IsInCheckmate(color, board):
        possibleMoves = allFuncs.colorSight(board, color)

        if not possibleMoves:
            return True
        else:
            return False