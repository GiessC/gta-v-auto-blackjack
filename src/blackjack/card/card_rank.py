from enum import Enum
import random


class CardRank(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

    def get_value(self) -> int:
        if self == CardRank.TWO:
            return 2
        if self == CardRank.THREE:
            return 3
        if self == CardRank.FOUR:
            return 4
        if self == CardRank.FIVE:
            return 5
        if self == CardRank.SIX:
            return 6
        if self == CardRank.SEVEN:
            return 7
        if self == CardRank.EIGHT:
            return 8
        if self == CardRank.NINE:
            return 9
        if self in [CardRank.TEN, CardRank.JACK, CardRank.QUEEN, CardRank.KING]:
            return 10
        if self == CardRank.ACE:
            return 11

    @staticmethod
    def random():
        return random.choice(list(CardRank))