from random import randrange


class Game:

    def __init__(self, player, deck, logging=False):
        '''Initialize the game'''
        self.player = player
        self.bet_amount = max(1, randrange(round(player.money * 0.05), round(player.money * 0.3)))
        self.deck = deck
        self.pool = 0
        self.logging = logging

    def __str__(self):
        return f"Poker Game for {self.player.name} with {len(self.deck)} remaining cards on deck."

    def call(self):
        '''Remove players gold equal to bet amount'''
        self.player.bet(self.bet_amount)
        self.pool += (self.bet_amount*2)

    def start(self):
        '''Starting the game'''
        self.deck.shuffle()
        self.open_cards = []
        self.player_cards = []
        self.server = []
        for i in range(2):
            self.player_cards.append(self.deck.draw())
            self.server.append(self.deck.draw())
        for i in range(3):
            self.open_cards.append(self.deck.draw())
        self.call()

    def show(self):
        '''Show the shared cards on the table'''
        print(f"Betted Gold : {self.pool}")
        print("Cards on the Table")
        for card in self.open_cards:
            print(f"- {card}")
        print()

    def show_player_cards(self):
        '''Show players cards'''
        self.player.current_gold()
        print("Players Cards :")
        for card in self.player_cards:
            print(f"- {card}")
        print()

    def show_server_cards(self):
        '''Show servers cards (Debug Only)'''
        print("Server Cards :")
        for card in self.server:
            print(f"- {card}")
        print()

    def update_info(self, card, info):
        '''Assessing the strength of the cards '''
        if card.type == -1:
            info['joker'] = True
            return
        # assigning the rank
        if card.rank not in info['rank']:
            info['rank'][card.rank] = 1
        else:
            info['rank'][card.rank] += 1
        # assigning the type
        if card.type not in info['type']:
            info['type'][card.type] = 1
        else:
            info['type'][card.type] += 1

    def check_combination(self, info):
        '''From cards  strength, calculate the possible combination'''
        # this function still does not count the joker
        combination = [
            ["Have Pair", False],
            ["Have double Pairs", False],
            ["Have Tres", False],
            ["Have a Straight", False],# not done
            ["Have a Flush", False],
            ["Have Full House", False],
            ["Have Four of a Kind", False],
            ["Have a Straight-Flush", False],# not done
            ["Have Five of a Kind", False],
        ]
        # check pair or double pair, and 4 and 5 of a kind
        two_count = 0
        pair = False
        tres = False
        for i in info['rank']:
            # check pair existance
            if info['rank'][i] == 2:
                two_count += 1
                pair = True
            # check tres existance
            if info['rank'][i] == 3:
                tres = True
                combination[2][1] = True
            # check 4 0f a kind existance
            if info['rank'][i] == 4:
                combination[6][1] = True
            # check 5 of a kind existance
            if info['rank'][i] == 5:
                combination[8][1] = True
        # check double pairs existance
        if two_count >= 2:
            combination[1][1] = True
        elif two_count == 1:
            combination[0][1] = True

        # check full House
        if pair and tres:
            combination[5][1] = True

        # check flush
        for i in info['type']:
            if info['type'][i] >= 5:
                combination[4][1] = True

        # check straight and straight-flush
        info['rank'] = sorted(info['rank'])
        count = 0
        curr = None
        for i in info['rank']:
            if count == 0:
                count += 1
                curr = i
                continue
            if curr == (i - 1):
                count += 1
            else:
                count = 1
        if count >= 5:
            # straight true
            combination[3][1] = True

        result = {
            'message': "This ain't got nothing",
            'value': -1
        }
        for i, combo in enumerate(combination):
            if combo[1]:
                result['message'] = combo[0]
                result['value'] = i
        return result

    def check(self):
        '''End of the game, Calculate and Compare the strength of players and servers cards'''
        player_info = {
            'type': {},
            'rank': {},
            'joker': False
        }
        server_info = {
            'type': {},
            'rank': {},
            'joker': False
        }
        for card in self.open_cards:
            self.update_info(card, player_info)
            self.update_info(card, server_info)
        for card in self.player_cards:
            self.update_info(card, player_info)
        for card in self.server:
            self.update_info(card, server_info)

        Sresult = self.check_combination(server_info)
        Presult = self.check_combination(player_info)
        print(f"Server has {Sresult['message']}")
        print(f"Player has {Presult['message']}")
        if Sresult['value'] > Presult['value']:
            return False
        elif Sresult['value'] < Presult['value']:
            return True
        else:
            print("Draw")
            highestP = self.highest(self.player_cards)
            highestS = self.highest(self.server)
            print(f"Server best card {highestS}")
            print(f"Player best card {highestP}")
            if highestP.rank > highestS.rank:
                return True
            elif highestP.rank == highestS.rank:
                if highestP.type >= highestS.type:
                    return True
                else:
                    return False
            else:
                return False

    def highest(self, cards):
        '''Determine the strongest card in each player and server hands'''
        highest = cards[0]
        for card in cards[1:]:
            if card.rank > highest.rank:
                highest = card
            elif card.rank == highest.rank:
                if card.type > highest.type:
                    highest = card
        return highest

    def add_on_table(self):
        '''Adding one card to shared cards on the table'''
        self.open_cards.append(self.deck.draw())

    def show_current(self, end=False):
        '''Showing the current state of the game'''
        if self.logging or end:
            self.show_server_cards()
        self.show()
        self.show_player_cards()

    def play(self):
        '''Rundown play of the game'''
        called = True
        for i in range(2):
            self.show_current()
            print("Call (c) or Fold (f)?")
            while True:
                is_call = input()
                print()
                if is_call == 'c':
                    self.add_on_table()
                    self.call()
                    break
                elif is_call == 'f':
                    print("Player Folded.")
                    called = False
                    break
                else:
                    print("Invalid Input!")
            if called is False:
                break

        if called:
            self.show_current(True)
            winner = self.check()
            if winner:
                self.player.won(self.pool)
                print("Player Won the Game")
                print(f"Players Gold has increased to {self.player.money} gold")
            else:
                print("Player Lose, Server Won the Game")
                print(f"Players Gold has reduced to {self.player.money} gold")
        else:
            print("You Chicken!")


class Player:

    def __init__(self, name, money):
        self.name = name
        self.money = money

    def __str__(self):
        return f"Player {self.name} with {self.money} golds.\n"

    def bet(self, amount):
        self.money -= amount

    def won(self, amount):
        self.money += amount

    def current_gold(self):
        print(f"Player current gold is {self.money}")
