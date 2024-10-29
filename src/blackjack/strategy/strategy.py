from abc import ABC, abstractmethod
from blackjack.action.action import Action
from blackjack.card.card import Card
from blackjack.player.player_hand import PlayerHand


class Strategy(ABC):
    title: str

    def __init__(self, title: str):
        self.title = title

    @abstractmethod
    def get_best_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        pass
