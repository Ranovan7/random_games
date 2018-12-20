from random import shuffle


class Card:

    def __init__(self, type, value=0):
        self.type = type
        self.rank = value

    def __str__(self):
        if self.type == -1:
            return "Joker"
        types = ['Clubs', 'Diamond', 'Hearts', 'Spades']
        higher = ['Jack', 'Queen', 'King', 'Ace']
        if self.rank >= 11:
            rank = higher[self.rank - 11]
        else:
            rank = self.rank
        type = types[self.type]
        return f"{rank} of {type}"


class Deck:

    def __init__(self, joker=0):
        self.deck = []
        for i in range(4):
            for j in range(13):
                self.deck.append(Card(i, j+2))
        for i in range(joker):
            self.deck.append(Card(-1))

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        return f"This is a deck of {len(self.deck)} cards."

    def shuffle(self):
        shuffle(self.deck)

    def draw(self):
        return self.deck.pop()
