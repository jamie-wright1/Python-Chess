import pygame as game
import functions as func
import ui
import AI
from icecream import ic

funcs = func.allFuncs

WHITE, BLACK = 16, 8

def turn(color, board):
    run = True
    mouseDown = False
    coordinates = (0, 0)
    pieceSight = []
    moveInfo = func.move()
    moveInfo.colorOfMover =  color


    clock = game.time.Clock()

    while run == True:
        clock.tick(60)

        for event in game.event.get():
            button = game.mouse.get_pressed()

            if button[0] == True:
                coordinates = event.pos[0], event.pos[1]

                if mouseDown == False:
                    moveInfo.startPosition = int(coordinates[0]/75 + 1) + 8*(7 - int(coordinates[1]/75)) - 1
                    moveInfo.pieceMoving = board[moveInfo.startPosition]

                    if 0 < moveInfo.pieceMoving - moveInfo.colorOfMover <= 6:
                        mouseDown = True
                        pieceSight = funcs.validMoves(moveInfo.pieceMoving, moveInfo.startPosition, board)
                        board[moveInfo.startPosition] = 0
                    else:
                        moveInfo.startPosition = -1
                        moveInfo.pieceMoving= -1
            elif mouseDown == True:
                coordinates = (event.pos[0], event.pos[1])
                moveInfo.movePosition = int(coordinates[0]/75 + 1) + 8*(7 - int(coordinates[1]/75)) - 1

                for move in pieceSight:
                    if moveInfo.movePosition == move.movePosition:
                        if move.isPromotion == True:
                            board[moveInfo.movePosition] = moveInfo.pieceMoving + 4
                        else:
                            board[moveInfo.movePosition] = moveInfo.pieceMoving

                        return board
                    
                board[moveInfo.startPosition] = moveInfo.pieceMoving
                moveInfo.startPosition = -1
                moveInfo.pieceMoving= -1
                mouseDown = False
                pieceSight = []
                coordinates = (0, 0)

            if event.type == game.QUIT:
                quit()
    
        ui.drawBoard(ui.WIN, board, coordinates, moveInfo, pieceSight)

def twoPlayerMode(board):
    clock = game.time.Clock()
    checkmate = False

    while checkmate == False:
        board = turn(WHITE, board)

        if func.allFuncs.IsInCheckmate(BLACK, board) == True:
            checkmate = True
            continue

        board = turn(BLACK, board)

        if func.allFuncs.IsInCheckmate(WHITE, board) == True:
            checkmate = True

    for i in range(60):
        clock.tick(60)
        ui.endGame(ui.WIN, 8)

def AIMode(board):
    
    checkmate = False
    turnsPlayed = 1

    while checkmate == False:
        turn(WHITE, board)

        if func.allFuncs.IsInCheckmate(BLACK, board) == True:
            checkmate = True
            continue
        
        turnsPlayed+=1

        AI.AIMove(board, turnsPlayed, 0, 3)

        if func.allFuncs.IsInCheckmate(WHITE, board) == True:
            checkmate = True
        
        turnsPlayed += 1