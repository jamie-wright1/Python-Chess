import pygame as game

PIECESIZE = (75,75)

WIDTH, HEIGHT = 600, 600
WIN = game.display.set_mode((WIDTH, HEIGHT))

class BoardColors:
    WHITE = (232, 235, 239)
    BLACK = (85, 95, 110)
    PURPLE = (100, 100, 150)
    YELLOW = (250, 240, 25)
    BLUE = (30, 165, 175)
    GREY = (130, 160, 160)

    HIGHLIGHTEDSQUARE = game.Surface((75,75))
    HIGHLIGHTEDSQUARE.set_alpha(100)
    HIGHLIGHTEDSQUARE.fill(GREY)

    BASESQUARE = game.Surface((75,75))
    BASESQUARE.set_alpha(200)
    BASESQUARE.fill(PURPLE)

class PieceImages:
    BLACKKING = game.image.load('chessPieces/blackPieces/blackKing.png')
    BLACKKING = game.transform.scale(BLACKKING, PIECESIZE)

    BLACKQUEEN = game.image.load('chessPieces/blackPieces/blackQueen.png')
    BLACKQUEEN = game.transform.scale(BLACKQUEEN, PIECESIZE)

    BLACKROOK = game.image.load('chessPieces/blackPieces/blackRook.png')
    BLACKROOK = game.transform.scale(BLACKROOK, PIECESIZE)

    BLACKBISHOP = game.image.load('chessPieces/blackPieces/blackBishop.png')
    BLACKBISHOP = game.transform.scale(BLACKBISHOP, PIECESIZE)
    
    BLACKKNIGHT = game.image.load('chessPieces/blackPieces/blackKnight.png')
    BLACKKNIGHT = game.transform.scale(BLACKKNIGHT, PIECESIZE)
    
    BLACKPAWN = game.image.load('chessPieces/blackPieces/blackPawn.png')
    BLACKPAWN = game.transform.scale(BLACKPAWN, PIECESIZE)
    
    WHITEKING = game.image.load('chessPieces/whitePieces/whiteKing.png')
    WHITEKING = game.transform.scale(WHITEKING, PIECESIZE)
    
    WHITEQUEEN = game.image.load('chessPieces/whitePieces/whiteQueen.png')
    WHITEQUEEN = game.transform.scale(WHITEQUEEN, PIECESIZE)
    
    WHITEROOK = game.image.load('chessPieces/whitePieces/whiteRook.png')
    WHITEROOK = game.transform.scale(WHITEROOK, PIECESIZE)
    
    WHITEBISHOP = game.image.load('chessPieces/whitePieces/whiteBishop.png')
    WHITEBISHOP = game.transform.scale(WHITEBISHOP, PIECESIZE)
    
    WHITEKNIGHT = game.image.load('chessPieces/whitePieces/whiteKnight.png')
    WHITEKNIGHT = game.transform.scale(WHITEKNIGHT, PIECESIZE)
    
    WHITEPAWN = game.image.load('chessPieces/whitePieces/whitePawn.png')
    WHITEPAWN = game.transform.scale(WHITEPAWN, PIECESIZE)

def drawBoard(surface, board, coordinates, startPosition, pieceMoving, possibleMoves):
    coordinates = (coordinates[0]-37.5, coordinates[1] - 37.5)

    surface.fill(BoardColors.WHITE)

    g = 0
    for i in range(64):
        if ((i+g) % 2 == 1):
            game.draw.rect(surface, BoardColors.BLACK, game.Rect(75*(i%8), 525-75*g, 75, 75))
        
        if i % 8 == 7:
            g+=1

    if pieceMoving != -1:
        xSquare = startPosition % 8
        ySquare = int(startPosition / 8)

        draw = (75*(xSquare), 525-75*ySquare)
        surface.blit(BoardColors.BASESQUARE, draw)      

    for move in possibleMoves:
        xSquare = move.movePosition % 8
        ySquare = int(move.movePosition / 8)

        surface.blit(BoardColors.HIGHLIGHTEDSQUARE, (75*(xSquare), 525-75*ySquare))

    x = 0
    y = 525

    for square in board:
        match square:

            case 0:
                True
            case 9:
                surface.blit(PieceImages.BLACKPAWN, (x, y))
            case 10:
                surface.blit(PieceImages.BLACKKNIGHT, (x, y))
            case 11:
                surface.blit(PieceImages.BLACKBISHOP, (x, y))
            case 12:
                surface.blit(PieceImages.BLACKROOK, (x, y))
            case 13:
                surface.blit(PieceImages.BLACKQUEEN, (x, y))
            case 14:
                surface.blit(PieceImages.BLACKKING, (x, y))
            case 17:
                surface.blit(PieceImages.WHITEPAWN, (x, y))
            case 18:
                surface.blit(PieceImages.WHITEKNIGHT, (x, y))
            case 19:
                surface.blit(PieceImages.WHITEBISHOP, (x, y))
            case 20:
                surface.blit(PieceImages.WHITEROOK, (x, y))
            case 21:
                surface.blit(PieceImages.WHITEQUEEN, (x, y))
            case 22:
                surface.blit(PieceImages.WHITEKING, (x, y))

        x+=75

        if x == 600:
            y-=75
            x=0
    
    if pieceMoving != - 1:
        match pieceMoving:

            case 0:
                True
            case 9:
                surface.blit(PieceImages.BLACKPAWN, (coordinates[0], coordinates[1]))
            case 10:
                surface.blit(PieceImages.BLACKKNIGHT, (coordinates[0], coordinates[1]))
            case 11:
                surface.blit(PieceImages.BLACKBISHOP, (coordinates[0], coordinates[1]))
            case 12:
                surface.blit(PieceImages.BLACKROOK, (coordinates[0], coordinates[1]))
            case 13:
                surface.blit(PieceImages.BLACKQUEEN, (coordinates[0], coordinates[1]))
            case 14:
                surface.blit(PieceImages.BLACKKING, (coordinates[0], coordinates[1]))
            case 17:
                surface.blit(PieceImages.WHITEPAWN, (coordinates[0], coordinates[1]))
            case 18:
                surface.blit(PieceImages.WHITEKNIGHT, (coordinates[0], coordinates[1]))
            case 19:
                surface.blit(PieceImages.WHITEBISHOP, (coordinates[0], coordinates[1]))
            case 20:
                surface.blit(PieceImages.WHITEROOK, (coordinates[0], coordinates[1]))
            case 21:
                surface.blit(PieceImages.WHITEQUEEN, (coordinates[0], coordinates[1]))
            case 22:
                surface.blit(PieceImages.WHITEKING, (coordinates[0], coordinates[1]))

    game.display.update()

def introScreen(surface):
    surface.fill(BoardColors.WHITE)
    
    font = game.font.SysFont("default", 50)
    font2 = game.font.SysFont("Times New Roman", 25)

    Intro = font.render("Welcome to Chess!", 1, BoardColors.BLACK)
    choice1 = font2.render("Play vs AI", 1, BoardColors.GREY)
    choice2 = font2.render("Play vs Mode", 1, BoardColors.GREY)
    choice3 = font2.render("Quit", 1, BoardColors.GREY)

    surface.blit(Intro, (50, 100))
    surface.blit(choice1, (50, 250))
    surface.blit(choice2, (50, 350))
    surface.blit(choice3, (50, 450))

    game.display.update()

def endGame(surface, color):
    if color == 8:
        colorStr = "White"
    else:
        colorStr = "Black"

    surface.fill(BoardColors.WHITE)

    font = game.font.SysFont("default", 50)

    checkmatePrint = font.render("Checkmate: " + colorStr + "wins!", 1, BoardColors.BLUE)

    surface.blit(checkmatePrint, (100, 200))

    game.display.update()