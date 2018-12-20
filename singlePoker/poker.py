from deck import Deck
from table import Player, Game

if __name__ == "__main__":
    print("Welcome to Single Player Poker!")
    print("You going to play againts the server which theoretically have infinite money.\n")
    print("The amount of bet is fixed each game.\n")
    print("Ready?")
    name = 'romy'  # input("Enter your name here : ")

    player = Player(name, 100)
    print(f"Player : {player}")
    game_num = 0
    while True:
        print(f"Game Number {game_num+1}\n")
        game = Game(player, Deck())

        game.start()
        game.play()

        game_num += 1
        break
