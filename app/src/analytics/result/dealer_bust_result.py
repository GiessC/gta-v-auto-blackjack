from analytics.result.result import ResultType
from analytics.result.win_result import WinResult


class DealerBustResult(WinResult):
    def __init__(self, player_total: int, dealer_total: int):
        super().__init__(player_total, dealer_total, ResultType.DEALER_BUST)

    def __str__(self) -> str:
        return "Dealer busts. Player wins."
