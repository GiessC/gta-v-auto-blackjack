from blackjack.exceptions.blackjack_exception import BlackjackException


class InvalidStateException(BlackjackException):
    def __init__(self, message: str):
        super().__init__(message)
