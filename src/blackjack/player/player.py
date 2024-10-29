from abc import ABC
from typing import Dict
from uuid import UUID, uuid4

from blackjack.player.player_hand import PlayerHand
from blackjack.strategy.strategy import Strategy
from blackjack.exceptions.not_enough_chips_exception import NotEnoughChipsException


class Player(ABC):
    active_hands: Dict[UUID, PlayerHand]
    closed_hands: Dict[UUID, PlayerHand]
    chip_count: int
    initial_bet: int
    strategy: Strategy

    def __init__(self, strategy: Strategy, initial_bet: int, chip_count: int):
        self.active_hands = {}
        self.closed_hands = {}
        self.initial_bet: int = initial_bet
        self.chip_count: int = chip_count
        self.strategy: Strategy = strategy

    def place_bet(self, amount: int):
        print(f'Placing bet of ${amount}')
        if (self.chip_count < amount):
            return NotEnoughChipsException(self.chip_count, amount)
        self.chip_count -= amount

    def add_chips(self, amount: int):
        self.chip_count += amount

    def split_hand(self, hand_id: UUID) -> UUID:
        self.place_bet(self.active_hands[hand_id].bet_amount)
        new_hand = PlayerHand(self.active_hands[hand_id].bet_amount)
        new_hand.cards.append(self.active_hands[hand_id].pop_card(0))
        new_hand_id = uuid4()
        self.active_hands[new_hand_id] = new_hand
        return new_hand_id

    def close_hand(self, hand_id: UUID):
        self.closed_hands[hand_id] = self.active_hands.pop(hand_id)

    def clear_hands(self):
        self.active_hands.clear()
        self.closed_hands.clear()

    def can_play(self) -> bool:
        for hand_index in self.active_hands:
            if self.active_hands[hand_index].can_play():
                return True
        return False

    def print_hands(self):
        for hand_index in self.active_hands:
            print(self.active_hands[hand_index])

