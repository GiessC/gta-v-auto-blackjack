from analytics.result.result import Result, ResultType


class WinResult(Result):
    def __init__(self, player_total: int, dealer_total: int, result_type: ResultType = ResultType.WIN):
        super().__init__(player_total, dealer_total, result_type)

    def __str__(self) -> str:
        return f"Dealer has {self.dealer_total}. Player has {self.player_total}. Player wins."
