# Necessary imports
import random


# Global array for the number values of non-numeric cards
count_values = {"A": 1, "J": 10, "Q": 10, "K": 10}
for i in range(2, 11):
    count_values[str(i)] = i

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


def CheckForFifteens(hand, target=15):
    if target == 0:
        return 1
    elif hand == [] or target < 0:
        return 0
    else:
        s = 0
        for c, card in enumerate(hand):
            s += CheckForFifteens(hand[c+1:], target - card)
        return s

class Cribbage:
    def __init__(self):
        self.deck = MakeDeck()
        random.shuffle(self.deck)
        # Player structure is their hand and then their score
        self.players = [[[], 0] for i in range(2)]
        # The last card of the crib will be the card from the deck
        # The other 4 cards come from the player's hands
        self.crib = []
        # crib_owner is their position in self.players (i.e. 0 or 1)
        self.crib_owner = 0
        self.values = {"A": 1, "J": 11, "Q": 12, "K": 13}
        for i in range(2, 11):
            self.values[str(i)] = i

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

    def ScoreHand(self, hand):
        """This method is used to calculate the score a hand would make during
           the show
        """
        score = 0
        # Pair check
        for c, card in enumerate(hand[:-1]):
            for pair_card in hand[c+1:]:
                if card[:-1] == pair_card[:-1]:
                    score += 2

        # Knob check
        for knob in hand[:-1]:
            if knob[:-1] == "J" and knob[-1] == hand[-1][-1]:
                score += 1

        # Run check
        hand.sort(key=lambda x: self.values[x[:-1]])
        for i, card in enumerate(hand):
            run_length = 1
            last_card = card
            for run_card in hand[i + 1:]:
                if self.values[run_card[:-1]] == self.values[last_card[:-1]] + 1:
                    run_length += 1
                    last_card = run_card
                else:
                    break
            if run_length >= 3:
                score += run_length
                break

        # Flush check
        full_flush = False
        for c, card in enumerate(hand[:-1]):
            if card[-1] != hand[c + 1][-1]:
                break
        else:
            score += 5
            full_flush = True
        if not full_flush:
            for c, card in enumerate(hand[:-2]):
                if card[-1] != hand[c + 1][-1]:
                    break
            else:
                score += 4

        # 15 Check
        hand_values = [count_values[i[:-1]] for i in hand]
        score += CheckForFifteens(hand_values) * 2
        return score

    def PlayRound(self):
        total = 0
        while total < 31:
            for player in self.players:
                # Change here for getting the best card to play at any time
                card_index = random.randint(0, len(player[1]) - 1)
                card = player[1].pop(card_index)

                if card[0] == "A":
                    total += 1
                elif card[0] == "J" or card[0] == "Q" or card[0] == "K":
                    total += 10




if __name__ == "__main__":
    game = Cribbage()
    # game.DealCards()
    # game.AddToCrib()
    # print(game.players)
    # print(game.crib)

    # Score Testing
    assert game.ScoreHand(["JD", "5H", "5S", "5C", "5D"]) == 29
    assert game.ScoreHand(["AD", "5H", "4D", "9S", "JH"]) == 6 # 
    assert game.ScoreHand(["AH", "5H", "4D", "9S", "JH"]) == 6
    assert game.ScoreHand(["AD", "JH", "4D", "9S", "5H"]) == 7
    assert game.ScoreHand(["AH", "8H", "3H", "7H", "5H"]) == 9
    assert game.ScoreHand(["2D", "AD", "JD", "9D", "QH"]) == 4
    assert game.ScoreHand(["AH", "AD", "JH", "KD", "AD"]) == 6
    print("All Tests passed")