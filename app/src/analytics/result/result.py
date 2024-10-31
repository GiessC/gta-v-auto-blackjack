from enum import Enum


class ResultType(Enum):
    PUSH = "push"
    PLAYER_BUST = "player_bust"
    DEALER_BUST = "dealer_bust"
    PLAYER_BLACKJACK = "player_blackjack"
    DEALER_BLACKJACK = "dealer_blackjack"
    WIN = "win"
    LOSS = "loss"
    UNKNOWN = "unknown"


class Result:
    result_type: ResultType
    bet: int
    player_total: int
    dealer_total: int

    def __init__(self, player_total: int, dealer_total: int, bet: int, result_type: ResultType):
        self.player_total = player_total
        self.dealer_total = dealer_total
        self.bet = bet
        self.result_type = result_type
