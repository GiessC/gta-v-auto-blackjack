from blackjack.card.card import Card
from blackjack.card.card_rank import CardRank


class CardFactory:
    @staticmethod
    def create_two() -> Card:
        return Card(CardRank.TWO, 2)

    @staticmethod
    def create_three() -> Card:
        return Card(CardRank.THREE, 3)

    @staticmethod
    def create_four() -> Card:
        return Card(CardRank.FOUR, 4)

    @staticmethod
    def create_five() -> Card:
        return Card(CardRank.FIVE, 5)

    @staticmethod
    def create_six() -> Card:
        return Card(CardRank.SIX, 6)

    @staticmethod
    def create_seven() -> Card:
        return Card(CardRank.SEVEN, 7)

    @staticmethod
    def create_eight() -> Card:
        return Card(CardRank.EIGHT, 8)

    @staticmethod
    def create_nine() -> Card:
        return Card(CardRank.NINE, 9)

    @staticmethod
    def create_ten() -> Card:
        return Card(CardRank.TEN, 10)

    @staticmethod
    def create_jack() -> Card:
        return Card(CardRank.JACK, 10)

    @staticmethod
    def create_queen() -> Card:
        return Card(CardRank.QUEEN, 10)

    @staticmethod
    def create_king() -> Card:
        return Card(CardRank.KING, 10)

    @staticmethod
    def create_ace() -> Card:
        return Card(CardRank.ACE, 11, 1)

    card_map = {
        CardRank.TWO: create_two,
        CardRank.THREE: create_three,
        CardRank.FOUR: create_four,
        CardRank.FIVE: create_five,
        CardRank.SIX: create_six,
        CardRank.SEVEN: create_seven,
        CardRank.EIGHT: create_eight,
        CardRank.NINE: create_nine,
        CardRank.TEN: create_ten,
        CardRank.JACK: create_jack,
        CardRank.QUEEN: create_queen,
        CardRank.KING: create_king,
        CardRank.ACE: create_ace,
    }

    @staticmethod
    def create_card_from_rank(rank: CardRank) -> Card:
        if rank not in CardFactory.card_map:
            raise ValueError(f'Invalid card rank: {rank}')
        return CardFactory.card_map[rank]()

    @staticmethod
    def random() -> Card:
        return CardFactory.create_card_from_rank(CardRank.random())
