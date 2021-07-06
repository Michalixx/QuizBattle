# -*- coding: utf-8 -*-
from network import Network
from game import Game
import pygame as pg
import time

pg.init()
width = 1280
height = 720
background_color = (139, 69, 19)
screen = pg.display.set_mode((width, height))
pg.display.set_caption("QuizBattle")
screen.fill(background_color)
pg.display.update()
inputBox = ""
result_font = pg.font.SysFont("comicsansms", 40)
question_font = pg.font.SysFont("timesnewroman", 50)
game = None


def text_wrapping(text):
    i = 0
    words = text.split()
    line  = ""
    while len(words) > 0:
        line_backup = line
        line += words[0]
        line += " "
        word_backup = words[0]
        words.remove(word_backup)
        lineRender = question_font.render(str(line), True, (255, 255, 255))
        if lineRender.get_width() > width:
            lineRender = question_font.render(str(line_backup), True, (255, 255, 255))
            screen.blit(lineRender, ((width - lineRender.get_width()) / 2, 100+60*i))
            i += 1
            line = ""
            line += word_backup
    if line != "":
        lineRender = question_font.render(str(line), True, (255, 255, 255))
        screen.blit(lineRender, ((width - lineRender.get_width()) / 2, 100 + 60 * i))


def draw_gui(player_number, question, inputBox):
    global game
    if player_number == 1:
        myScore = game.player1_correct
        myTotal = game.player1_total
        enemyScore = game.player2_correct
        enemyTotal = game.player2_total
    else:
        myScore = game.player2_correct
        myTotal = game.player2_total
        enemyScore = game.player1_correct
        enemyTotal = game.player1_total

    time = int(game.get_time())

    myText = result_font.render(str(myScore) + "/" + str(myTotal), True, (255, 255, 255))
    enemyText = result_font.render(str(enemyScore) + "/" + str(enemyTotal), True, (255, 255, 255))
    timeText = result_font.render(str(time), True, (255,255,255))
    text_wrapping(question)
    screen.blit(myText, (5, 5))
    screen.blit(enemyText, (width - 5 - enemyText.get_width(), 5))
    text_surf = result_font.render(inputBox, True, (255, 0, 0))
    screen.blit(text_surf, ((width - text_surf.get_width()) / 2, (height - text_surf.get_height()) / 2))
    screen.blit(timeText, ((width - timeText.get_width()) / 2, 5))


def draw_end_screen(player_number, question):
    global game
    if player_number == 1:
        myScore = game.player1_correct
        myTotal = game.player1_total
        enemyScore = game.player2_correct
        enemyTotal = game.player2_total
    else:
        myScore = game.player2_correct
        myTotal = game.player2_total
        enemyScore = game.player1_correct
        enemyTotal = game.player1_total



    myText = result_font.render(str(myScore) + "/" + str(myTotal), True, (255, 255, 255))
    enemyText = result_font.render(str(enemyScore) + "/" + str(enemyTotal), True, (255, 255, 255))
    endText = question_font.render("Thanks for playing :D", True, (255,255,255))
    screen.blit(myText, (5, 5))
    screen.blit(enemyText, (width - 5 - enemyText.get_width(), 5))
    screen.blit(endText, ((width - endText.get_width()) / 2, (height - endText.get_height()) / 2))


def main():
    global inputBox
    global game
    n = Network()
    player_number, question, game = n.data
    print("Waiting for opponent")
    print("I am player", player_number)

    run = True
    while run:
        screen.fill(background_color)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    print("back")
                    inputBox = inputBox[:-1]
                elif (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER) and inputBox != "":
                    question, game = n.send(inputBox)
                    inputBox = ""
                elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    pass
                else:
                    inputBox += event.unicode

        try:
            question, game = n.send("get")
        except:
            break

        if game.get_end():
            draw_end_screen(player_number, question)

        elif game.get_status():
            draw_gui(player_number, question, inputBox)
        else:
            waitingText = result_font.render("Waiting for opponent...", True, (255, 255, 255))
            screen.blit(waitingText, ((width - waitingText.get_width()) / 2, (height - waitingText.get_height()) / 2))

        pg.display.update()


main()
