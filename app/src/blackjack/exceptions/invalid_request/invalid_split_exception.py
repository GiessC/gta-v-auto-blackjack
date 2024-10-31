from blackjack.exceptions.invalid_request.invalid_request_exception import InvalidRequestException


class InvalidSplitException(InvalidRequestException):
    def __init__(self, reason: str):
        super().__init__("split hand", reason)