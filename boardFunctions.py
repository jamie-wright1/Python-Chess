import pieces

class boardFuncs:
    startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def createBoard():
        board = []

        for i in range(64):
            board.append(0)

        return board

    def fenToBoard(Fen, board = None, color = None, castling = None, enPassant = None):
        i = 0

        for m in Fen:
            
            match m:
                case 'p':
                    board[i] = pieces.white | pieces.pawn
                case 'P':
                    board[i] = pieces.black | pieces.pawn
                case 'r':
                    board[i] = pieces.white | pieces.rook
                case 'R':
                    board[i] = pieces.black | pieces.rook
                case 'n':
                    board[i] = pieces.white | pieces.knight
                case 'N':
                    board[i] = pieces.black | pieces.knight
                case 'b':
                    board[i] = pieces.white | pieces.bishop
                case 'B':
                    board[i] = pieces.black | pieces.bishop
                case 'q':
                    board[i] = pieces.white | pieces.queen
                case 'Q':
                    board[i] = pieces.black | pieces.queen
                case 'k':
                    board[i] = pieces.white | pieces.king
                case 'K':
                    board[i] = pieces.black | pieces.king
                case '/':
                    i-=1
                case ' ':
                    break
                case _:
                    integer = int(m)
                    i += integer - 1
            
            i += 1

        #board.reverse()
        
    def boardToFen(board):
        True

    def updateBoard(move, board):
        savePiece = board[move[1]]

        if pieces.pawnPromotion(move, board) == True:
            board[move[1]] = board[move[0]] + 4
        else:
            board[move[1]] = board[move[0]]

        board[move[0]] = 0
        
        return savePiece
    
    def undoMove(move, board, savedPiece):
        board[move[0]] = board[move[1]]
        board[move[1]] = savedPiece
    
    def placePieces():
        board = []

        for _ in range(64):
            board.append(0)
            
        boardFuncs.fenToBoard(boardFuncs.startFen, board)

        return board