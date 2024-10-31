from abc import ABC
from typing import List

from analytics.counters.win_loss_counter import WinLossCounter
from blackjack.card.card import Card
from blackjack.player.player_hand import PlayerHand
from blackjack.player.pub_sub.player_observer import PlayerObserver
from blackjack.strategy.strategy import Strategy
from blackjack.exceptions.not_enough_chips_exception import NotEnoughChipsException
from utils.pub_sub.observable import Observable


class Player(ABC, Observable[PlayerObserver]):
    name: str = 'Player'
    hands: List[PlayerHand]
    chip_count: int
    strategy: Strategy
    win_loss: WinLossCounter

    def __init__(self, strategy: Strategy, chip_count: int):
        super().__init__()
        self.hands = []
        self.win_loss = WinLossCounter()
        self.chip_count: int = chip_count
        self.strategy: Strategy = strategy

    def add_hand(self, hand: PlayerHand):
        hand.attach(self.win_loss)

    def play_hands(self, dealer_upcard: Card):
        reversed_hands = reversed(self.hands)
        for hand in reversed_hands:
            print(f'Playing [{hand}]:')
            while hand.can_play():
                action = self.strategy.get_best_move(hand, dealer_upcard)
                new_hand = hand.perform(action)
                if new_hand:
                    self.hands.append(new_hand)
        self.notify_hands_played()

    def play(self, bet_amount: int, dealer_upcard: Card):
        self.place_bet(bet_amount)
        self.play_hands(dealer_upcard)

    def place_bet(self, amount: int):
        if (self.chip_count < amount):
            return NotEnoughChipsException(self.chip_count, amount)
        self.chip_count -= amount
        self.notify_bet_placed(amount)

    def hands_to_string(self):
        string = ''
        for hand in self.hands:
            string += f'\n\t{hand}'
        return string

    def notify_bet_placed(self, amount: int):
        for observer in self.observers:
            observer.on_bet_placed(self, amount)

    def notify_hands_played(self):
        for observer in self.observers:
            observer.on_hands_played(self)
