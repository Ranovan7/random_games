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
    is_stop = False
    game_num = 0
    while True:
        print(f"GAME NUMBER {game_num+1}\n")
        game = Game(player, Deck(), False)
        game.start()
        game.play()
        game_num += 1

        if player.money < 3:
            print("Your Gold is too low, you cannot play anymore")
            break

        print("Play again? (y/n)")
        while True:
            rematch = input()
            if rematch == 'y':
                print("Next game")
                break
            elif rematch == 'n':
                print("Thanks for Playing, have a good day.")
                is_stop = True
                break
            else:
                print("Invalid Input!")
        print()
        if is_stop:
            break
