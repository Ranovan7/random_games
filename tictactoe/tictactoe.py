from board import Board

if __name__ == "__main__":
    print("Welcome to the Game of Tic Tac Toe")
    player = ['X', 'O']
    x = input("Enter dimension of the board :")
    game = Board(int(x))
    game.view()

    turn = 0
    while True:
        print(f"Turn number {turn+1}")
        print(f"Player {(turn % 2) + 1} Move")
        print("Vertical as first number, Horizontal as second number!")
        while True:
            new_input = input("Select board number :")
            check = game.update(new_input, player[turn % 2])
            if check is True:
                break
            else:
                print("Try Again")
        turn += 1
        game.view()
        if game.endgame:
            break
