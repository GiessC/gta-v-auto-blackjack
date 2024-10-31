from typing import Dict, Set, Tuple
from blackjack.action.action import Action, ActionType
from blackjack.card.card import Card
from blackjack.player.player_hand import PlayerHand
from blackjack.settings.blackjack_settings import BlackjackSettings
from blackjack.strategy.strategy import Strategy


class BasicStrategy(Strategy):
    pair_splitting: Dict[int, bool | Set[int]]
    soft_totals: Dict[int | Tuple[int, int], ActionType]
    settings: BlackjackSettings

    def __init__(self, settings: BlackjackSettings):
        super().__init__("Basic Strategy")
        self.settings = settings
        self.pair_splitting = {
            11: True,
            10: False,
            9: { 2, 3, 4, 5, 6, 8, 9 },
            8: True,
            7: { 2, 3, 4, 5, 6, 7 },
            6: { 3, 4, 5, 6 },
            5: False,
            4: False,
            3: { 4, 5, 6, 7 },
            2: { 4, 5, 6, 7 },
        }
        if (self.settings.can_double_after_split):
            self.pair_splitting[4] = { 5, 6 }
            self.pair_splitting[6].add(2)
            self.pair_splitting[3].add(2)
            self.pair_splitting[3].add(3)
            self.pair_splitting[2].add(2)
            self.pair_splitting[2].add(3)
        self.soft_totals = {}
        self.soft_totals[9]       = Action(ActionType.STAND)
        self.soft_totals[(8, 2)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 3)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 4)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 5)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 6)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(8, 7)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 8)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 9)]  = Action(ActionType.STAND)
        self.soft_totals[(8, 10)] = Action(ActionType.STAND)
        self.soft_totals[(8, 11)] = Action(ActionType.STAND)
        self.soft_totals[(7, 2)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(7, 3)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(7, 4)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(7, 5)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(7, 6)]  = Action(ActionType.DOUBLE, ActionType.STAND)
        self.soft_totals[(7, 7)]  = Action(ActionType.STAND)
        self.soft_totals[(7, 8)]  = Action(ActionType.DOUBLE, ActionType.HIT)
        self.soft_totals[(6, 3)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(6, 4)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(6, 5)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(6, 6)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(5, 4)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(5, 5)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(5, 6)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(4, 4)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(4, 5)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(4, 6)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(3, 5)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(3, 6)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(2, 5)]  = Action(ActionType.DOUBLE)
        self.soft_totals[(2, 6)]  = Action(ActionType.DOUBLE)


    def should_split(self, player_hand: PlayerHand, dealer_upcard: Card) -> bool:
        pair_rank: int = player_hand.cards[0].max_value
        if (self.pair_splitting[pair_rank] == False):
            return False
        return self.pair_splitting[pair_rank] == True or dealer_upcard.rank in self.pair_splitting[pair_rank]

    def get_soft_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if player_hand.total - 11 > 8:
            return Action(ActionType.STAND)
        if (player_hand.total - 11, dealer_upcard.max_value) in self.soft_totals:
            return self.soft_totals[(player_hand.total - 11, dealer_upcard.max_value)]
        if player_hand.total - 11 in self.soft_totals:
            return self.soft_totals[player_hand.total - 11]
        return Action(ActionType.HIT)

    def get_hard_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if player_hand.total >= 17:
            return Action(ActionType.STAND)
        if player_hand.total <= 8:
            return Action(ActionType.HIT)
        if player_hand.total >= 13 and player_hand.total <= 16 and dealer_upcard.max_value <= 6:
            return Action(ActionType.STAND)
        if player_hand.total == 12 and dealer_upcard.max_value >= 4 and dealer_upcard.max_value <= 6:
            return Action(ActionType.STAND)
        if self.settings.can_double:
            if player_hand.total == 11:
                return Action(ActionType.DOUBLE)
            if player_hand.total == 10 and dealer_upcard.max_value <= 9:
                return Action(ActionType.DOUBLE)
            if player_hand.total == 9 and dealer_upcard.max_value >= 3 and dealer_upcard.max_value <= 6:
                return Action(ActionType.DOUBLE)
        return Action(ActionType.HIT)

    def get_best_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if player_hand.is_pair() and self.should_split(player_hand, dealer_upcard):
            return Action(ActionType.SPLIT)
        if player_hand.is_soft():
            return self.get_soft_move(player_hand, dealer_upcard)
        return self.get_hard_move(player_hand, dealer_upcard)

