'''module that stores the board object for tictactoe game'''
class Board():
    '''Board Class'''

    def __init__(self, n):
        '''Initializing the Board'''
        n = max(min(n, 5), 3)
        self.board = []
        self.win_point = n
        self.endgame = False
        self.winner = None
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(" ")
            self.board.append(temp)

    def check_end(self, height, width):
        '''Checking for the condition which the game should end'''
        current_player = self.board[height][width]
        # check for Horizontal
        count = 0
        for i in range(self.win_point):
            if self.board[height][i] == current_player:
                count += 1
            else:
                break
        if count >= self.win_point:
            self.endgame = True
            self.winner = current_player
            return

        # check for Vertical
        count = 0
        for i in range(self.win_point):
            if self.board[i][width] == current_player:
                count += 1
            else:
                break
        if count >= self.win_point:
            self.endgame = True
            self.winner = current_player
            return

        # check for Diagonal 1
        count = 0
        for i in range(self.win_point):
            if self.board[i][i] == current_player:
                count += 1
            else:
                break
        if count >= self.win_point:
            self.endgame = True
            self.winner = current_player
            return

        # check for Diagonal 2
        count = 0
        for i in range(self.win_point):
            if self.board[i][(self.win_point - 1) - i] == current_player:
                count += 1
            else:
                break
        if count >= self.win_point:
            self.endgame = True
            self.winner = current_player
            return

        # check for Draw
        is_draw = True
        for i in self.board:
            for j in i:
                if j not in ("X", "O"):
                    is_draw = False
                    break
            if not is_draw:
                break
        if is_draw:
            self.endgame = True
            self.winner = "Draw"

    def view(self):
        '''Showing the state of the Board'''
        temp = ""
        for i in range(self.win_point+1):
            temp += "[{}]  ".format(i)
        print(temp, "\n")
        for i, num in enumerate(self.board):
            line = " "
            for j in num:
                line += f"[{j}]  "
            print([i+1], line, "\n")

    def update(self, code, player):
        '''Updating the state of the Board'''
        if len(code) > 2 or len(code) < 2:
            print("Input Length not correct !")
            return False
        else:
            index = list(code)
            height = int(index[0])-1
            width = int(index[1])-1
            if height >= self.win_point or width >= self.win_point:
                print("The Board is not that Huge!")
                return False
            else:
                value = self.board[height][width]
                if value not in ("X", "O"):
                    self.board[height][width] = player
                    print("Correct input !\n")
                else:
                    print("The Board section already populated!")
                    return False
        self.check_end(height, width)
        if self.winner:
            if self.winner == "Draw":
                print("GAME OVER\n")
                print("The Game is Draw!\n")
            else:
                print("GAME OVER\n")
                print(f"Congratulation for Player {self.winner} for winning the game!\n")
        return True
