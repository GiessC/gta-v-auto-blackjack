from typing import List
from uuid import UUID, uuid4

from blackjack.action.action import Action, ActionType
from blackjack.card.card import Card
from blackjack.card.card_factory import CardFactory
from blackjack.exceptions.invalid_request.invalid_split_exception import InvalidSplitException
from blackjack.player.pub_sub.player_hand_observer import PlayerHandObserver
from utils.pub_sub.observable import Observable


MAX_TOTAL: int = 21

class PlayerHand(Observable[PlayerHandObserver]):
    id: UUID
    cards: List[Card]
    total: int
    stood: bool
    bet_amount: int

    def __init__(self, bet_amount: int, id: UUID = uuid4()):
        super().__init__()
        self.id = id
        self.cards = []
        self.total = 0
        self.stood = False
        self.bet_amount = bet_amount

    def perform(self, action: Action) -> 'PlayerHand':
        if action.action_type == ActionType.HIT:
            # card = self.controller.hit_and_wait_for_card()
            card = CardFactory.random()
            print(f'Player hit: {card}')
            self.hit(card)
        elif action.action_type == ActionType.STAND:
            print(f'Player stood on hand: {self}')
            self.stand()
        elif action.action_type == ActionType.DOUBLE:
            # card = self.controller.double_and_wait_for_card()
            card = CardFactory.random()
            print(f'Player doubled down on hand: {self} and hit: {card}')
            self.double_down(card)
        elif action.action_type == ActionType.SPLIT:
            print(f'Player split hand: {self}')
            return self.split()
        else:
            raise Exception(f'Tried to perform invalid action on player hand: {action}')
        return None

    def add_card(self, card: Card):
        self.hit(card)

    def hit(self, card: Card):
        self.cards.append(card)
        card_value = card.max_value
        if self.total + card.max_value > MAX_TOTAL:
            card_value = card.min_value
        self.total += card_value

    def stand(self):
        self.stood = True

    def double_down(self, card: Card):
        self.hit(card)
        self.bet_amount *= 2

    def split(self) -> 'PlayerHand':
        self.check_splitable()
        split_hand = PlayerHand(self.bet_amount)
        split_hand.hit(self.cards.pop())
        return split_hand

    def check_splitable(self):
        if len(self.cards) != 2:
            raise InvalidSplitException("Player can only split with two cards")
        if self.cards[0].max_value != self.cards[1].max_value:
            raise InvalidSplitException("Player can only split with two cards of the same rank")

    def can_play(self) -> bool:
        return not self.stood and self.total < MAX_TOTAL

    def is_bust(self) -> bool:
        return self.total > MAX_TOTAL

    def is_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].max_value == self.cards[1].max_value

    def is_soft(self) -> bool:
        total = self.total
        found_ace = False
        for card in self.cards:
            if card.is_ace() and not found_ace:
                total -= 10
                found_ace = True
        return total < 12

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.total == MAX_TOTAL

    def notify_card_added(self, card: Card):
        for observer in self.observers:
            observer.on_card_added(self, card)

    def __str__(self) -> str:
        string = ', '.join([str(card) for card in self.cards])
        return string + f'. Total: {self.total}'
