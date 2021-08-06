# Necessary imports
import random


def MakeDeck():
    """This function returns an ordered deck of cards"""
    deck = []
    for suit in ["S", "H", "C", "D"]:
        for index in range(1, 14):
            if index == 1:
                deck.append("A" + suit)
            elif index == 11:
                deck.append("J" + suit)
            elif index == 12:
                deck.append("Q" + suit)
            elif index == 13:
                deck.append("K" + suit)
            else:
                deck.append(str(index) + suit)
    return deck


class Cribbage:
    def __init__(self):
        self.deck = MakeDeck()
        random.shuffle(self.deck)
        # Player structure is their hand and then their score
        self.players = [[[], 0] for i in range(2)]
        self.crib = []
        # crib_owner is their position in self.players (i.e. 0 or 1)
        self.crib_owner = 0

    def DealCards(self):
        """Method that deals cards to each player"""
        for i in range(6):
            for player in self.players:
                player[0].append(self.deck.pop())

    def AddToCrib(self):
        """Method that adds cards from the player's hand to the crib.
           Currently, this is the last two cards the player was dealt but
           if this class is inherited, this method can be overridden to create
           strategy
        """
        for i in range(2):
            for player in self.players:
                self.crib.append(player[0].pop())
        self.crib.append(self.deck.pop())


if __name__ == "__main__":
    game = Cribbage()
    game.DealCards()
    game.AddToCrib()
    print(game.players)
    print(game.crib)
