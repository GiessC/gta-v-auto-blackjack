from typing import override

from read.chip_reader.chip_reader import ChipReader

class InputChipReader(ChipReader):
    MAX_TRIES = 3
    tries: int = 0

    @override
    def read_chips(self) -> int:
        try:
            chips = int(input('How many chips do you have? $'))
            self.tries = 0
            return chips
        except ValueError:
            if self.tries == InputChipReader.MAX_TRIES:
                print(f'Too many invalid inputs. Max tries ({InputChipReader.MAX_TRIES}) exceeded. Exiting...')
                exit(1)
            print('Invalid input. Please enter a number.')
            self.tries += 1
            return self.read_chips()
