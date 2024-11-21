from random import shuffle

class Deck:
    def __init__(self):
        self.deck = self.deck_contructor()
        self.deck_shuf()

    def deck_contructor(self):
        numbers = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        suits = ['s','d','c','h']
        deck = []
        for n in numbers:
            for s in suits:
                deck.append(n + s)
        return deck

    def add_card(self, card):
        self.deck.append(card)
        self.deck_shuf()

    def deck_shuf(self):
        shuffle(self.deck)

    def remove_top_card(self):
        card = self.deck[0]
        self.deck.pop(0)
        return card

    def remove_specific_card(self, card):
        self.deck.pop(self.deck.index(card))
