from analytics.result.loss_result import LossResult
from analytics.result.result import ResultType


class PlayerBustResult(LossResult):
    def __init__(self, player_total: int, dealer_total: int):
        super().__init__(player_total, dealer_total, ResultType.PLAYER_BUST)

    def __str__(self) -> str:
        return "Player busts. Dealer wins."
