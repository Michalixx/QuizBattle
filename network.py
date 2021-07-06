import socket
import pickle
from game import Game

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.24"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.data = self.connect()
        self.player_number = self.data[0]

    def connect(self):
        try:
            self.client.connect(self.addr)
            player_number, game_status = pickle.loads(self.client.recv(2048))
            self.player_number = player_number
            return player_number, game_status[0], game_status[1]
        except:
            return 1, 2, 3

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            ret = pickle.loads(self.client.recv(2048*8))
            return ret
        except socket.error as e:
            print(e)

    def get_player_number(self):
        return self.player_number

