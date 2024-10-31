from blackjack.player.player import Player
from blackjack.settings.blackjack_settings import BlackjackSettings
from blackjack.strategy.basic_strategy import BasicStrategy


class BasicStrategyPlayer(Player):
    def __init__(self, settings: BlackjackSettings, chip_count: int):
        super().__init__(BasicStrategy(settings), chip_count)
