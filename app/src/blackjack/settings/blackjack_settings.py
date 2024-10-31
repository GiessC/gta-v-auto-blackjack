from enum import Enum

class ChipReadMethod(Enum):
    INPUT = "input"
    _EXPERIMENTAL_OCR = "__experimental_ocr"

class BlackjackSettings:
    chip_read_method: ChipReadMethod
    stop_at_loss_gte: int
    bet_amount: int
    can_double: bool
    can_double_after_split: bool
    can_surrender: bool
    _simulate: bool

    def __init__(
        self,
        stop_at_loss_gte: int = 1_000_000,
        chip_read_method = ChipReadMethod.INPUT,
        bet_amount: int = 50_000,
        can_double: bool = True,
        can_double_after_split: bool = True,
        can_surrender: bool = False
    ):
        self.stop_at_loss_gte = stop_at_loss_gte
        self.bet_amount = bet_amount
        self.can_double = can_double
        self.can_double_after_split = can_double_after_split
        self.can_surrender = can_surrender
        self.chip_read_method = chip_read_method
        self._simulate = False

        self.validate()

    def validate(self):
        if not self.can_double and self.can_double_after_split:
            raise ValueError("Can't double after split (DAS) if doubling is disabled.")
