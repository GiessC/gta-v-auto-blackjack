from analytics.result.result import Result, ResultType


class WinResult(Result):
    multiplier: float

    def __init__(self, player_total: int, dealer_total: int, bet: int, multiplier: float = 1.0, result_type: ResultType = ResultType.WIN):
        self.multiplier = multiplier
        super().__init__(player_total, dealer_total, bet, result_type)

    def __str__(self) -> str:
        return f"Dealer has {self.dealer_total}. Player has {self.player_total}. Player wins."
