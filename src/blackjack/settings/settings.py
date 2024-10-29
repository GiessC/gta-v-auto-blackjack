class Settings:
    bet_amount: int
    can_double: bool
    can_double_after_split: bool
    can_surrender: bool

    def __init__(self, bet_amount: int = 50_000, can_double: bool = True, can_double_after_split: bool = True, can_surrender: bool = False):
        self.bet_amount = bet_amount
        self.can_double = can_double
        self.can_double_after_split = can_double_after_split
        self.can_surrender = can_surrender

        self.validate()

    def validate(self):
        if not self.can_double and self.can_double_after_split:
            raise ValueError("Can't double after split (DAS) if doubling is disabled.")
