from blackjack.exceptions.blackjack_exception import BlackjackException


class NotEnoughChipsException(BlackjackException):
    def __init__(self, chip_count: int, amount: int):
        super().__init__(f'Player does not have enough chips! Chip count: {chip_count}, amount: {amount}')
        self.chip_count = chip_count
        self.amount = amount
