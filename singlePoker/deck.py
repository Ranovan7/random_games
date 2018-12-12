
class Card:

    def __init__(self, type, value=0):
        self.type = type
        self.value = value

    def __str__(self):
        if self.type == -1:
            return "Joker"
        types = ['Clubs', 'Diamond', 'Hearts', 'Spades']
        higher = ['Jack', 'Queen', 'King', 'Ace']
        if self.value >= 11:
            rank = higher[self.value - 11]
        else:
            rank = self.value
        type = types[self.type]
        return f"{rank} of {type}"


class Deck:

    def __init__():
        pass


somecard = Card(1, 14)
print(somecard)
somecard2 = Card(-1)
print(somecard2)
