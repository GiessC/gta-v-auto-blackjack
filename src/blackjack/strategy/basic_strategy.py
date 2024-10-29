from typing import Dict, Set, Tuple
from blackjack.action.action import Action, ActionType
from blackjack.card.card import Card
from blackjack.card.card_rank import CardRank
from blackjack.player.player_hand import PlayerHand
from blackjack.settings.settings import Settings
from blackjack.strategy.strategy import Strategy


class BasicStrategy(Strategy):
    pair_splitting: Dict[CardRank, bool | Set[CardRank]]
    soft_totals: Dict[int | Tuple[int, int], ActionType]
    settings: Settings

    def __init__(self, settings: Settings):
        super().__init__("Basic Strategy")
        self.settings = settings
        self.pair_splitting = {
            CardRank.ACE:   True,
            CardRank.TEN:   False,
            CardRank.NINE:  { CardRank.TWO, CardRank.THREE, CardRank.FOUR, CardRank.FIVE, CardRank.SIX, CardRank.EIGHT, CardRank.NINE },
            CardRank.EIGHT: True,
            CardRank.SEVEN: { CardRank.TWO, CardRank.THREE, CardRank.FOUR, CardRank.FIVE, CardRank.SIX, CardRank.SEVEN },
            CardRank.SIX:   { CardRank.THREE, CardRank.FOUR, CardRank.FIVE, CardRank.SIX },
            CardRank.FIVE:  False,
            CardRank.FOUR:  False,
            CardRank.THREE: { CardRank.FOUR, CardRank.FIVE, CardRank.SIX, CardRank.SEVEN },
            CardRank.TWO:   { CardRank.FOUR, CardRank.FIVE, CardRank.SIX, CardRank.SEVEN },
        }
        if (self.settings.can_double_after_split):
            self.pair_splitting[CardRank.FOUR] = { CardRank.FIVE, CardRank.SIX }
            self.pair_splitting[CardRank.SIX].add(CardRank.TWO)
            self.pair_splitting[CardRank.THREE].add(CardRank.TWO)
            self.pair_splitting[CardRank.THREE].add(CardRank.THREE)
            self.pair_splitting[CardRank.TWO].add(CardRank.TWO)
            self.pair_splitting[CardRank.TWO].add(CardRank.THREE)
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
        pair_rank: CardRank = player_hand.cards[0].rank
        if (self.pair_splitting[pair_rank] == False):
            return False
        return self.pair_splitting[pair_rank] == True or dealer_upcard.rank in self.pair_splitting[pair_rank]

    def get_soft_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if (player_hand.total() - CardRank.ACE.get_value(), dealer_upcard.max_value) in self.soft_totals:
            return Action(self.soft_totals[(player_hand.total() - CardRank.ACE.get_value(), dealer_upcard.max_value)])
        if player_hand.total() - CardRank.ACE.get_value() in self.soft_totals:
            return Action(self.soft_totals[player_hand.total() - CardRank.ACE.get_value()])
        return Action(ActionType.HIT)

    def get_hard_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if player_hand.total() >= 17:
            return Action(ActionType.STAND)
        if player_hand.total() <= 8:
            return Action(ActionType.HIT)
        if player_hand.total() >= 13 and player_hand.total() <= 16 and dealer_upcard.max_value <= 6:
            return Action(ActionType.STAND)
        if player_hand.total() == 12 and dealer_upcard.max_value >= 4 and dealer_upcard.max_value <= 6:
            return Action(ActionType.STAND)
        if self.settings.can_double:
            if player_hand.total() == 11:
                return Action(ActionType.DOUBLE)
            if player_hand.total() == 10 and dealer_upcard.max_value <= 9:
                return Action(ActionType.DOUBLE)
            if player_hand.total() == 9 and dealer_upcard.max_value >= 3 and dealer_upcard.max_value <= 6:
                return Action(ActionType.DOUBLE)
        return Action(ActionType.HIT)

    def get_best_move(self, player_hand: PlayerHand, dealer_upcard: Card) -> Action:
        if player_hand.is_pair() and self.should_split(player_hand, dealer_upcard):
            return Action(ActionType.SPLIT)
        if player_hand.is_soft():
            return self.get_soft_move(player_hand, dealer_upcard)
        return self.get_hard_move(player_hand, dealer_upcard)

