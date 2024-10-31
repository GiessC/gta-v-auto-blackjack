from blackjack.player.player import Player
from blackjack.player.pub_sub.player_observer import PlayerObserver


class ProfitCounter(PlayerObserver):
    profit: int

    def __init__(self, player: Player, starting_profit: int = 0):
        player.attach(self)
        self.profit = starting_profit

    def add(self, profit: int):
        self.profit += profit

    def subtract(self, profit: int):
        self.profit -= profit

    def count(self) -> int:
        return self.profit

    def on_bet_placed(self, player, amount: int):
        self.subtract(amount)

    def on_win(self, player, amount: int):
        self.add(amount)