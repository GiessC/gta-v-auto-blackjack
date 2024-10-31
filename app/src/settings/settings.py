from blackjack.settings.blackjack_settings import BlackjackSettings
from read.settings.ocr_settings import OCRSettings


class Settings:
    ocr_settings: OCRSettings
    blackjack_settings: BlackjackSettings

    def __init__(self):
        self.blackjack_settings = BlackjackSettings()
