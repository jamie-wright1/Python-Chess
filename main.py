import pygame as game
from pygame import font as fonts
import boardFunctions
import functions as funcs
import ui as ui
import gameModes as mode

board = boardFunctions.boardFuncs

game.display.set_caption("Chess")

FPS = 60

def main():
    boardState = board.placePieces()

    fonts.init()

    ui.introScreen(ui.WIN)

    game.init()
    
    clock = game.time.Clock()

    run = True

    end = False

    while (run):
        clock.tick(FPS)

        for event in game.event.get():
            mouseCoors = game.mouse.get_pos()
            button = game.mouse.get_pressed()

            if button[0] == True:
                if 50 < mouseCoors[0] < 155 and 250 < mouseCoors[1] < 275:
                    mode.AIMode(boardState)
                    end = True
                elif 50 < event.pos[0] < 190 and 350 < event.pos[1] < 375:
                    mode.twoPlayerMode(boardState)
                    run = False
                elif 50 < event.pos[0] < 100 and 450 < event.pos[1] < 475:
                    run = False
                
            if event.type == game.QUIT:
                run = False
        
        if end == True:
            ui.endGame(ui.WIN, 16)
        else:
            ui.introScreen(ui.WIN)

main()