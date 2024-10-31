import random
from blackjack.card.card import Card


class CardFactory:
    def create_two():
        return Card(2, 2)

    def create_three():
        return Card(3, 3)

    def create_four():
        return Card(4, 4)

    def create_five():
        return Card(5, 5)

    def create_six():
        return Card(6, 6)

    def create_seven():
        return Card(7, 7)

    def create_eight():
        return Card(8, 8)

    def create_nine():
        return Card(9, 9)

    def create_ten():
        return Card(10, 10)

    def create_ace():
        return Card(11, 1)

    def random():
        max_value = random.randint(2, 11)
        return Card(max_value, 1 if max_value == 11 else max_value)
