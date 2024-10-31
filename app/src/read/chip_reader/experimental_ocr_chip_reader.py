from typing import Tuple, override

import pyautogui
from read.areas.blackjack_areas import Areas, Position
from read.chip_reader.chip_reader import ChipReader
from read.image.image_finder import ImageFinder
from read.image.image_reader import ImageReader
from read.settings.ocr_settings import OCRSettings


class ExperimentalOCRChipReader(ChipReader, ImageFinder, ImageReader):
    chips_icon_path = 'src/resources/img/chips_icon.png'

    def __init__(self, settings: OCRSettings):
        super().__init__(settings)

    def find_chips_icon(self) -> Position:
        return self.find_image(ExperimentalOCRChipReader.chips_icon_path)

    @override
    def read_chips(self) -> int:
        chip_icon_coords: Tuple[int, int, int, int] = self.find_chips_icon()
        chips_area: Position = Areas.get_chips_area(chip_icon_coords)
        image = pyautogui.screenshot(region=chips_area.to_tuple())
        chips = self.read_int_from_image(image)
        return chips
