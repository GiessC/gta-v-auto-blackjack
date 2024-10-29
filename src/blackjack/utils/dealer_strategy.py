from blackjack.action.action import Action, ActionType
from blackjack.player.player_hand import PlayerHand
from blackjack.strategy.strategy import Strategy


class DealerStrategy(Strategy):
    def __init__(self):
        super().__init__("Dealer Strategy")

    def get_best_move(self, player_hand: PlayerHand, _) -> Action:
        if player_hand.total() < 17:
            return Action(ActionType.HIT)
        return Action(ActionType.STAND)