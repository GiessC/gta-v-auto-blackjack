from analytics.result.result import Result, ResultType


class LossResult(Result):
    def __init__(self, player_total: int, dealer_total: int, bet: int, result_type: ResultType = ResultType.LOSS):
        super().__init__(player_total, dealer_total, bet, result_type)

    def __str__(self) -> str:
        return f"Dealer has {self.dealer_total}. Player has {self.player_total}. Player loses."
