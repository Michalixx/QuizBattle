from network import Network
from game import Game

def play_game(player_number, question, game):
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

    print("My score:", myScore, "/", myTotal)
    print("Enemy score:", enemyScore, "/", enemyTotal)
    print("Question:", question)
    ans = input()
    return ans


def main():
    n = Network()
    player_number, question, game = n.data
    print("Waiting for opponent")
    while True:
        print(game.get_status())
        if game.get_status():
            ans = play_game(player_number, question, game)
            n.send(ans)

main()





