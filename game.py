import random

QUESTIONS = []


def generate_question():
    for i in range(100):
        quest = str(i)
        QUESTIONS.append((quest + "+" + quest + "=", i+i))


def load_questions_from_file(filename):
    file = open(filename, "r")
    for line in file:
        str = line.split("@")
        QUESTIONS.append((str[0], str[1].strip().lower()))
    random.shuffle(QUESTIONS)

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
        if ans.lower() == QUESTIONS[self.player1_total][1]:
            self.player1_total += 1
            self.player1_correct += 1
            return True
        else:
            self.player1_total += 1
            return False

    def submit_player2_answer(self, ans):
        if ans.lower() == QUESTIONS[self.player2_total][1]:
            self.player2_total += 1
            self.player2_correct += 1
            return True
        else:
            self.player2_total += 1
            return False

    def game_status(self, player):
        if player == 1:
            return (QUESTIONS[self.player1_total][0], self)
        else:
            return (QUESTIONS[self.player2_total][0], self)


load_questions_from_file("question_set_1")
generate_question()
