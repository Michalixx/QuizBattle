import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.24"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

player_counter = 0
game = Game(1)
print(game)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server started.")


def threaded_client(conn, player_number):
    conn.send(pickle.dumps((player_number, game.game_status(player_number))))

    while True:
        try:
            data = conn.recv(4096).decode()
            if player_number == 1:
                game.submit_player1_answer(int(data))
                replay = game.game_status()
                conn.sendall(pickle.dumps(replay))
            else:
                game.submit_player2_answer(int(data))
                replay = game.game_status()
                conn.sendall(pickle.dumps(replay))
        except:
            break


while True:
    conn, addr = s.accept()
    player_counter += 1
    print("Player", player_counter, "connected")
    if player_counter == 2:
        game.set_status_on()
        print("New game status", game.get_status())
    start_new_thread(threaded_client, (conn, player_counter))

