class Card:
    max_value: int
    min_value: int

    def __init__(self, max_value: int, min_value: int | None = None):
        self.max_value = max_value
        self.min_value = min_value if min_value is not None else max_value

    def __str__(self) -> str:
        if self.is_ace():
            return 'A'
        return f'{self.max_value}'

    def is_ace(self) -> bool:
        return self.max_value == 11
