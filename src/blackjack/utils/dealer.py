from typing import List, override
from uuid import UUID, uuid4
from blackjack.action.action import Action, ActionType
from blackjack.card.card import Card
from blackjack.exceptions.blackjack_exception import BlackjackException
from blackjack.player.player import Player
from blackjack.player.player_hand import PlayerHand
from blackjack.utils.deck import Deck
from blackjack.utils.dealer_strategy import DealerStrategy
from blackjack.card.card_factory import CardFactory


class Dealer(Player):
    deck: Deck

    def __init__(self):
        super().__init__(DealerStrategy(), 0, 0)
        self.deck = Deck()
        self.chip_count: int = 0

    def command(self, action: Action, player: Player, hand_id: UUID):
        if action.action_type == ActionType.HIT:
            player.active_hands[hand_id].try_add_card(self.deck.draw())
        elif action.action_type == ActionType.SPLIT:
            new_hand_id = player.split_hand(hand_id)
            player.active_hands[new_hand_id].try_add_card(self.deck.draw())
            player.active_hands[hand_id].try_add_card(self.deck.draw())
        elif action.action_type == ActionType.DOUBLE:
            player.place_bet(player.active_hands[hand_id].bet_amount)
            player.active_hands[hand_id].try_add_card(self.deck.draw())
            player.close_hand(hand_id)
        if action.action_type in [ActionType.STAND, ActionType.DOUBLE]:
            player.close_hand(hand_id)


    def get_upcard(self) -> Card | None:
        if not self.active_hands:
            return None
        hand = next(iter(self.active_hands.values())) # Dealer can only have one hand
        if len(hand.cards) < 2:
            return None
        return hand.cards[1]

    def deal_players(self, players: List[Player]):
        for player in players:
            # self.deal_player(player)
            player.active_hands[uuid4()] = PlayerHand(
                player.initial_bet,
                [
                    CardFactory.create_ace(),
                    CardFactory.create_ace(),
                ]
            )
        self.deal_player(self)


    def deal_player(self, player: Player):
        player.active_hands[uuid4()] = PlayerHand(
            player.initial_bet,
            [
                self.deck.draw(),
                self.deck.draw(),
            ]
        )

    @override
    def place_bet(self, _: int):
        pass
