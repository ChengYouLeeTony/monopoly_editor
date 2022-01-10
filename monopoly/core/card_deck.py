from .card import Card
from random import shuffle

class CardDeck(object):

    # property
    def __init__(self):
        self._index = 0
        self._cards = []

    def get_cards(self):
        return self._cards

    def insert(self, card):
        self._cards.append(card)

    def shuffle(self):
        shuffle(self._cards)

    def draw(self):
        self._index = (self._index + 1) % len(self._cards)
        if self._index == 0:
            self.shuffle()
        return self._cards[self._index]
