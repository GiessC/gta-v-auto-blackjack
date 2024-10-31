from typing import Tuple

import pyautogui


class Areas:
    def get_chips_area(chip_icon_coords: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        screen_width, _ = pyautogui.size()
        return (chip_icon_coords[2] + 2, chip_icon_coords[1] - 10, screen_width - chip_icon_coords[2], chip_icon_coords[3] - chip_icon_coords[1] + 20)

