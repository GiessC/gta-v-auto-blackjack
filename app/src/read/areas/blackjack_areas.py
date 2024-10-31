from typing import Tuple

import pyautogui

from read.image.image_finder import Position

class Areas:
    # HelpMessage = Position(128, 72, 565, 59)
    HelpMessage = Position(1515, 142, 265, 35)
    # BetAmount = Position(2241, 1264, 192, 52) # TODO: Adjust this amount to not include 'BET'
    BetAmount = Position(2384, 863, 79, 31)

    def get_chips_area(chip_icon_coords: Tuple[int, int, int, int]) -> Position:
        screen_width, _ = pyautogui.size()
        return Position(chip_icon_coords[2] + 2, chip_icon_coords[1] - 10, screen_width - chip_icon_coords[2], chip_icon_coords[3] - chip_icon_coords[1] + 20)

