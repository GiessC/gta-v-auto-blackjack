from analytics.result.result import Result, ResultType


class PushResult(Result):
    def __init__(self, total: int):
        super().__init__(total, total, ResultType.PUSH)

    def __str__(self) -> str:
        return f"Dealer and Player have {self.player_total}. The game is a push."
