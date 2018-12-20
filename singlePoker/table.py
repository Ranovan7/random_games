from random import randrange


class Game:

    def __init__(self, player, deck):
        self.player = player
        self.bet_amount = randrange(round(player.money * 0.1), round(player.money * 0.4))
        self.deck = deck
        self.pool = 0

    def __str__(self):
        return f"Poker Game for {self.player.name} with {len(self.deck)} remaining cards on deck."

    def call(self):
        self.player.bet(self.bet_amount)
        self.pool += (self.bet_amount*2)

    def start(self):
        self.deck.shuffle()
        self.open_cards = []
        self.player_cards = []
        self.server = []
        for i in range(2):
            self.player_cards.append(self.deck.draw())
            self.server.append(self.deck.draw())
        for i in range(5):
            self.open_cards.append(self.deck.draw())

    def show(self):
        for card in self.open_cards:
            print(f"- {card}")
        print()

    def show_player_cards(self):
        print("Your Cards :")
        for card in self.player_cards:
            print(f"- {card}")
        print()

    def show_server_cards(self):
        print("Server Cards :")
        for card in self.server:
            print(f"- {card}")
        print()

    def update_info(self, card, info):
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
        # this function still does not count the joker
        combination = [
            ["Have Pair", False],
            ["Have double Pairs", False],
            ["Have Tres", False],
            ["Have a Straight", False],
            ["Have a Flush", False],
            ["Have Full House", False],
            ["Have Four of a Kind", False],
            ["Have a Straight-Flush", False],
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
        if Sresult['value'] > Presult['value']:
            return False
        elif Sresult['value'] < Presult['value']:
            return True
        else:
            highestP = self.highest(self.player_cards)
            highestS = self.highest(self.server)
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
        highest = cards[0]
        for card in cards[1:]:
            if card.rank > highest.rank:
                highest = card
            elif card.rank == highest.rank:
                if card.type > highest.type:
                    highest = card
        print(highest)
        return highest

    def show_current(self):
        self.show_server_cards()
        self.show()
        self.show_player_cards()

    def play(self):
        called = True
        for i in range(3):
            self.show_current()
            print("Call (c) or Fold (f)?")
            is_call = input()
            if is_call == 'c':
                continue
            elif is_call == 'f':
                print("Player Folded.")
                called = False
                break
            else:
                print("Invalid Input!")
        if called:
            winner = self.check()
            if winner:
                print("Player Won the Game")
            else:
                print("Player Lose, Server Won the Game")
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
