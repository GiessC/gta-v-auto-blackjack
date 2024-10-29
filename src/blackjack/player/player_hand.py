from enum import Enum
from typing import List, Set
from blackjack.card.card import Card
from blackjack.card.card_rank import CardRank


class BlackjackResult(Enum):
    PUSH = 0
    WIN = 1
    BLACKJACK = 2
    LOSS = 3
    BUST = 4

class PlayerHand:
    cards: List[Card]
    ace_indices: Set[int] = set()
    finished: bool = False
    bet_amount: int
    result: BlackjackResult

    def __init__(self, bet_amount: int, cards: List[Card] = []):
        self.bet_amount = bet_amount
        self.cards = []
        for card in cards:
            self.try_add_card(card)

    def pop_card(self, index: int):
        return self.cards.pop(index)

    def total(self) -> int:
        total = 0
        for i, card in enumerate(self.cards):
            if card.rank == CardRank.ACE:
                self.ace_indices.add(i)
            total += card.max_value
        while total > 21 and len(self.ace_indices) > 0:
            ace_index = self.ace_indices.pop()
            self.ace_indices.add(ace_index)
            total -= 10
        return total

    def try_add_card(self, card: Card) -> int:
        self.cards.append(card)

        if self.total() > 21:
            self.result = BlackjackResult.BUST
        elif self.is_blackjack():
            self.result = BlackjackResult.BLACKJACK

    def can_play(self) -> bool:
        return self.total() < 21 and not self.finished

    def is_blackjack(self) -> bool:
        if len(self.cards) != 2:
            return False
        return self.total() == 21

    def is_pair(self) -> bool:
        if len(self.cards) != 2:
            return False
        return self.cards[0].rank == self.cards[1].rank

    def is_soft(self) -> bool:
        if len(self.ace_indices) == 0:
            return False
        ace_index = self.ace_indices.pop()
        self.ace_indices.add(ace_index)

        rest_total = 0
        for i, card in enumerate(self.cards):
            if i != ace_index:
                rest_total += card.max_value
        return rest_total + 11 <= 21

    # A, 9, 7
    def __str__(self):
        return ", ".join([str(card) for card in self.cards] + [f'Total: {self.total()}'])
