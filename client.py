# -*- coding: utf-8 -*-
from network import Network
from game import Game
import pygame as pg
import pygame_menu
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
text_color = (128, 0, 128)
point_color = (245,245,220)
answer_color = (192, 192, 192)
enemy_disconnected_color = (255, 0, 0)
time_color = (176,196,222)
game = None

NICKNAME = ""


def text_wrapping(text):
    i = 0
    words = text.split()
    line = ""
    while len(words) > 0:
        line_backup = line
        line += words[0]
        line += " "
        word_backup = words[0]
        words.remove(word_backup)
        lineRender = question_font.render(str(line), True, text_color)
        if lineRender.get_width() > width:
            lineRender = question_font.render(str(line_backup), True, text_color)
            screen.blit(lineRender, ((width - lineRender.get_width()) / 2, 100 + 60 * i))
            i += 1
            line = ""
            line += word_backup
    if line != "":
        lineRender = question_font.render(str(line), True, text_color)
        screen.blit(lineRender, ((width - lineRender.get_width()) / 2, 100 + 60 * i))


def draw_gui(player_number, n):
    global game
    inputbox = ""
    running = True
    while running:
        question, game = n.send("get")

        for event in pg.event.get():
            if event.type == pg.QUIT:
                n.only_send("disconnect")
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    inputbox = inputbox[:-1]
                elif (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER) and inputbox != "":
                    return inputbox
                elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    pass
                else:
                    inputbox += event.unicode

        if player_number == 1:
            myScore = game.player1_correct
            myTotal = game.player1_total
            enemyScore = game.player2_correct
            enemyTotal = game.player2_total
            myNick = game.get_p1nick()
            enemyNick = game.get_p2nick()
        else:
            myScore = game.player2_correct
            myTotal = game.player2_total
            enemyScore = game.player1_correct
            enemyTotal = game.player1_total
            myNick = game.get_p2nick()
            enemyNick = game.get_p1nick()

        time = int(game.get_time())

        if game.disconnected:
            enemyColor = enemy_disconnected_color
        else:
            enemyColor = point_color

        screen.fill(background_color)
        myText = result_font.render(str(myNick) + ": " + str(myScore) + "/" + str(myTotal), True, point_color)
        enemyText = result_font.render(str(enemyNick) + ": " +  str(enemyScore) + "/" + str(enemyTotal), True,
                                       enemyColor)
        timeText = result_font.render(str(time), True, time_color)
        text_wrapping(question)
        screen.blit(myText, (5, 5))
        screen.blit(enemyText, (width - 5 - enemyText.get_width(), 5))
        text_surf = result_font.render(inputbox, True, answer_color)
        screen.blit(text_surf, ((width - text_surf.get_width()) / 2, (height - text_surf.get_height()) / 2))
        screen.blit(timeText, ((width - timeText.get_width()) / 2, 5))
        pg.display.update()


def draw_end_screen(player_number):
    global game

    running = True
    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        if player_number == 1:
            myScore = game.player1_correct
            myTotal = game.player1_total
            enemyScore = game.player2_correct
            enemyTotal = game.player2_total
            myNick = game.get_p1nick()
            enemyNick = game.get_p2nick()
        else:
            myScore = game.player2_correct
            myTotal = game.player2_total
            enemyScore = game.player1_correct
            enemyTotal = game.player1_total
            myNick = game.get_p2nick()
            enemyNick = game.get_p1nick()

        enemyColor = point_color
        if game.disconnected:
            enemyColor = answer_color

        screen.fill(background_color)
        myText = result_font.render(str(myNick) + ": " + str(myScore) + "/" + str(myTotal), True, point_color)
        enemyText = result_font.render(str(enemyNick) + ": " + str(enemyScore) + "/" + str(enemyTotal), True,
                                       enemyColor)
        endText = question_font.render("Thanks for playing :D", True, text_color)
        screen.blit(myText, (5, 5))
        screen.blit(enemyText, (width - 5 - enemyText.get_width(), 5))
        screen.blit(endText, ((width - endText.get_width()) / 2, (height - endText.get_height()) / 2))
        pg.display.update()


def draw_input_your_nickname():
    global NICKNAME
    inputbox = ""
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    inputbox = inputbox[:-1]
                elif (event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER) and inputbox != "":
                    NICKNAME = inputbox
                    running = False
                elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    pass
                else:
                    inputbox += event.unicode

        screen.fill(background_color)
        text = result_font.render("Enter your nickname:", True, text_color)
        screen.blit(text, ((width - text.get_width()) / 2, 50))
        text_surf = result_font.render(inputbox, True, answer_color)
        screen.blit(text_surf, ((width - text_surf.get_width()) / 2, (height - text_surf.get_height()) / 2))
        pg.display.update()


def draw_waiting_for_opponent():
    screen.fill(background_color)
    waitingText = result_font.render("Waiting for opponent...", True, text_color)
    screen.blit(waitingText, ((width - waitingText.get_width()) / 2, (height - waitingText.get_height()) / 2))
    pg.display.update()


def run_menu():
    menu = pygame_menu.menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input("Name:")
    menu.add.button("Play", main)
    menu.add.button('Quit')
    print('f')
    menu.mainloop(screen)
    print('XD')


def main():
    global inputBox
    global game

    draw_input_your_nickname()

    n = Network()
    player_number, question, game = n.data

    print("Waiting for opponent")
    print("I am player", player_number)

    n.send(str(NICKNAME))

    while True:
        question, game = n.send("get")

        if game.get_end():
            draw_end_screen(player_number)

        elif game.get_status():
            answer = draw_gui(player_number, n)
            question, game = n.send(answer)
        else:
            draw_waiting_for_opponent()

    # run = True
    # while run:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             run = False
    #             n.only_send("disconnect")
    #
    #     try:
    #         question, game = n.send("get")
    #     except:
    #         break
    #
    #     if game.get_end():
    #         draw_end_screen(player_number)
    #
    #     elif game.get_status():
    #         answer = draw_gui(player_number, question, n)
    #         question, game = n.send(answer)
    #     else:
    #         draw_waiting_for_opponent()
    #
    #     pg.display.update()


run_menu()
print('l')