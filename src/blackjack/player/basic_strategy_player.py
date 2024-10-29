from blackjack.player.player import Player
from blackjack.settings.settings import Settings
from blackjack.strategy.basic_strategy import BasicStrategy


class BasicStrategyPlayer(Player):
    def __init__(self, settings: Settings, initial_bet: int, chip_count: int):
        super().__init__(BasicStrategy(settings), initial_bet, chip_count)
