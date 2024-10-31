from typing import override

from read.chip_reader.chip_reader import ChipReader

class InputChipReader(ChipReader):
    MAX_TRIES = 3
    chips: int | None = None
    tries: int = 0

    def __init__(self, chips: int | None = None):
        self.chips = chips

    @override
    def read_chips(self) -> int:
        if self.chips is not None:
            return self.chips
        try:
            chips = int(input('How many chips do you have? $'))
            self.chips = chips
            self.tries = 0
            return chips
        except ValueError:
            if self.tries == InputChipReader.MAX_TRIES:
                print(f'Too many invalid inputs. Max tries ({InputChipReader.MAX_TRIES}) exceeded. Exiting...')
                exit(1)
            print('Invalid input. Please enter a number.')
            self.tries += 1
            return self.read_chips()
