import socket
from _thread import *
import pickle
from game import Game
import time

server = "192.168.1.24"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

player_counter = 0
game_counter = 0
games = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server started.")


def threaded_client(conn, player_number, game):
    conn.send(pickle.dumps((player_number, game.game_status(player_number))))

    while True:

        if game.get_status() and game.start_time == -1:
            game.start_time = time.time()

        if game.get_status() and not game.get_end():
            game.time = 5 - (time.time() - game.start_time)
            if game.time <= 0:
                game.end = True

        try:
            data = conn.recv(4096).decode()
            if data == "get":
                replay = game.game_status(player_number)
                conn.sendall(pickle.dumps(replay))
            elif player_number == 1:
                game.submit_player1_answer(data)
                replay = game.game_status(player_number)
                conn.sendall(pickle.dumps(replay))
            else:
                game.submit_player2_answer(data)
                replay = game.game_status(player_number)
                conn.sendall(pickle.dumps(replay))
        except:
            break


while True:
    conn, addr = s.accept()
    player_counter += 1
    if player_counter % 2 == 1:
        game_counter += 1
        games.append(Game(game_counter))
    print("Player", player_counter, "connected")
    if player_counter % 2 == 0:
        games[game_counter-1].set_status_on()
        print("New game status", games[game_counter-1].get_status())
    start_new_thread(threaded_client, (conn, ((player_counter+1) % 2)+1, games[game_counter-1]))

