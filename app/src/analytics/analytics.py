from typing import List
from analytics.counters.win_loss_counter import WinLossCounter
from analytics.result.result import Result
from blackjack.player.player import Player


class Analytics:
    player: Player
    win_loss_counter: WinLossCounter

    def __init__(self, player: Player):
        self.player = player
        self.win_loss_counter = WinLossCounter()

    def track_results(self, results: List[Result]):
        for result in results:
            self.win_loss_counter.on_result(result)

    def profit(self):
        return self.player.chip_count - self.player.starting_chip_count

    def __str__(self) -> str:
        string = ''

        string += str(self.win_loss_counter) + '\n'

        return string
