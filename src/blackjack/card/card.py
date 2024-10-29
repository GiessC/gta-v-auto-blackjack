from blackjack.card.card_rank import CardRank


class Card:
    rank: CardRank
    max_value: int
    min_value: int | None

    def __init__(self, rank: CardRank, maxValue: int, minValue: int | None = None):
        self.rank = rank
        self.max_value = maxValue
        self.min_value = maxValue if minValue is None else minValue

    def __str__(self) -> str:
        return f'{self.rank}'
