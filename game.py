QUESTIONS = [(1, "2+2=", 4), (2, "Jestem kozakiem?", 1)]

class Game:
    def __init__(self, id):
        self.id = id
        self.player1_correct = 0
        self.player1_total = 0
        self.player2_correct = 0
        self.player2_total = 0
        self.status = False

    def get_status(self):
        return self.status

    def set_status_on(self):
        self.status = True

    def submit_player1_answer(self, ans):
        if ans == QUESTIONS[self.player1_total][2]:
            self.player1_total += 1
            self.player1_correct += 1
            return True
        else:
            self.player1_total += 1
            return False

    def submit_player2_answer(self, ans):
        if ans == QUESTIONS[self.player2_total][2]:
            self.player2_total += 1
            self.player2_correct += 1
            return True
        else:
            self.player2_total += 1
            return False

    def game_status(self, player):
        if player == 1:
            return (QUESTIONS[self.player1_total], self)
        else:
            return (QUESTIONS[self.player2_total], self)
