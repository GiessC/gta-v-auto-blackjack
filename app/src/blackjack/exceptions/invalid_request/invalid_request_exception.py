class InvalidRequestException(Exception):
    def __init__(self, attempted_to: str, error_reason: str):
        super().__init__(f"Player attempted to {attempted_to}: {error_reason}.")
