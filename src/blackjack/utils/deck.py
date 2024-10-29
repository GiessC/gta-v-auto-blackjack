import random
from typing import List
from blackjack.card.card import Card
from blackjack.card.card_rank import CardRank


class Deck:
    cards: List[Card]

    def __init__(self):
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        self.cards = []
        for _ in range(4):
            for rank in CardRank.__members__.values():
                self.cards.append(Card(rank, rank.get_value()))

    def draw(self) -> Card:
        return self.cards.pop()

    def shuffle(self):
        random.shuffle(self.cards)