from analytics.result.result import ResultType
from analytics.result.win_result import WinResult


class PlayerBlackjackResult(WinResult):
    def __init__(self, dealer_total: int):
        super().__init__(21, dealer_total, ResultType.PLAYER_BLACKJACK)

    def __str__(self) -> str:
        return f"Dealer has {self.dealer_total}. Player wins with Blackjack."