import re
from typing import override

import pyautogui
from read.areas.blackjack_areas import Areas
from read.bet_reader.bet_reader import BetReader
from read.image.image_reader import ImageReader
from read.settings.ocr_settings import OCRSettings


class PositionalBetReader(BetReader, ImageReader):
    def __init__(self, ocr_settings: OCRSettings):
        super().__init__(ocr_settings)

    @override
    def read_bet_amount(self) -> int:
        image = pyautogui.screenshot(region=Areas.BetAmount.to_tuple())
        message = self.read_text_from_image(image)
        pattern = r"(\d+)"
        match = re.search(pattern, message)
        if match:
            print("Bet amount: ", match.group(1))
            return int(match.group(1))
        else:
            raise ValueError("Could not find bet amount on screen")