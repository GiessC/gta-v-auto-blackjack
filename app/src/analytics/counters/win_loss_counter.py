from analytics.result.loss_result import LossResult
from analytics.result.result import Result
from analytics.result.results_observer import ResultsObserver
from analytics.result.win_result import WinResult
from blackjack.player.player import Player
from blackjack.player.player_hand import PlayerHand


class WinLossCounter(ResultsObserver):
    wins: int
    losses: int

    def __init__(self):
        self.wins = 0
        self.losses = 0

    def on_win(self):
        self.wins += 1

    def on_loss(self):
        self.losses += 1

    def on_result(self, result: Result):
        if isinstance(result, WinResult):
            self.on_win()
        elif isinstance(result, LossResult):
            self.on_loss()
        else:
            return

    def get_percentage(self) -> float:
        total = self.wins + self.losses
        if total == 0:
            return 0
        return self.wins / total

    def __str__(self) -> str:
        return f"Wins: {self.wins}, Losses: {self.losses}, Win Percentage: {self.get_percentage() * 100:.2f}%"
