import pygame as game
import functions as func
import ui
import AI
import pieces

funcs = func

WHITE, BLACK = 16, 8

def turn(color, board):
    run = True
    mouseDown = False
    coordinates = (0, 0)
    pieceSight = []
    startPosition = -1
    pieceMoving = -1

    clock = game.time.Clock()

    while run == True:
        clock.tick(60)

        for event in game.event.get():
            button = game.mouse.get_pressed()

            if button[0] == True:
                coordinates = game.mouse.get_pos()

                if mouseDown == False:
                    startPosition = int(coordinates[0]/75 + 1) + 8*(7 - int(coordinates[1]/75)) - 1
                    pieceMoving = board[startPosition]

                    if 0 < pieceMoving - color <= 6:
                        mouseDown = True
                        if pieceMoving < 16:
                            pins = func.findPins(board, 16)
                            potentialSight = funcs.possibleAttacksOnKing(board, 16)
                        else:
                            pins = func.findPins(board, 8)
                            potentialSight = funcs.possibleAttacksOnKing(board, 8)
                        pieceSight = funcs.validMoves(pieceMoving, startPosition, board, pins, potentialSight)
                        board[startPosition] = 0
                    else:
                        startPosition = -1
                        pieceMoving= -1
            elif mouseDown == True:
                coordinates = game.mouse.get_pos()
                placeCoor = int(coordinates[0]/75 + 1) + 8*(7 - int(coordinates[1]/75)) - 1

                for move in pieceSight:
                    if placeCoor == move.movePosition:
                        if pieces.pawnPromotion(pieceMoving, placeCoor) == True:
                            board[placeCoor] = pieceMoving + 4
                        else:
                            board[placeCoor] = pieceMoving

                        startPosition = -1
                        pieceMoving= -1
                        pieceSight = []
                        coordinates = (0, 0)

                        ui.drawBoard(ui.WIN, board, coordinates, startPosition, pieceMoving, pieceSight)

                        return board
                    
                board[startPosition] = pieceMoving
                startPosition = -1
                pieceMoving= -1
                mouseDown = False
                pieceSight = []
                coordinates = (0, 0)

            if event.type == game.QUIT:
                quit()
    
        ui.drawBoard(ui.WIN, board, coordinates, startPosition, pieceMoving, pieceSight)

def twoPlayerMode(board):
    clock = game.time.Clock()
    checkmate = False

    while checkmate == False:
        board = turn(WHITE, board)

        if func.IsInCheckmate(BLACK, board) == True:
            checkmate = True
            continue

        board = turn(BLACK, board)

        if func.IsInCheckmate(WHITE, board) == True:
            checkmate = True

    for _ in range(60):
        clock.tick(60)
        ui.endGame(ui.WIN, 8)

def AIMode(board):
    
    checkmate = False
    turnsPlayed = 1

    while checkmate == False:
        turn(WHITE, board)

        if func.IsInCheckmate(BLACK, board) == True:
            checkmate = True
            continue
        
        turnsPlayed+=1

        AI.AIMove(board, turnsPlayed, 3)

        if func.IsInCheckmate(WHITE, board) == True:
            checkmate = True
        
        turnsPlayed += 1