from analytics.result.loss_result import LossResult
from analytics.result.result import ResultType


class DealerBlackjackResult(LossResult):
    def __init__(self, player_total: int):
        super().__init__(player_total, 21, ResultType.DEALER_BLACKJACK)

    def __str__(self) -> str:
        return f"Player has {self.player_total}. Dealer wins with Blackjack."