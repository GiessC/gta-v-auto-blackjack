import re
from typing import override

import pyautogui
from read.areas.blackjack_areas import Areas
from read.help_reader.help_reader import HelpReader
from read.image.image_reader import ImageReader
from read.settings.ocr_settings import OCRSettings


class PositionalHelpReader(HelpReader, ImageReader):
    def __init__(self, settings: OCRSettings):
        super().__init__(settings)

    @override
    def read_help_msg(self) -> int:
        image = pyautogui.screenshot(region=Areas.HelpMessage.to_tuple())
        message = self.read_text_from_image(image)
        return message

    @override
    def read_for_card_total(self) -> int:
        image = pyautogui.screenshot(region=Areas.HelpMessage.to_tuple())
        message = self.read_text_from_image(image)
        dealer_card_view_pattern = r"Dealer has (\d+)".replace(" ", "")
        match = re.search(dealer_card_view_pattern, message)
        if match:
            print("Dealer card total: ", match.group(1))
            return int(match.group(1))
        player_card_view_pattern = r"You have (\d+)".replace(" ", "")
        match = re.search(player_card_view_pattern, message)
        if match:
            print("Player card total: ", match.group(1))
            return int(match.group(1))
        raise ValueError("Could not find card total in help message")