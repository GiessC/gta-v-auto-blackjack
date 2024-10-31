from abc import ABC, abstractmethod
from read.image.image_reader import ImageReader
from read.settings.ocr_settings import OCRSettings


class BetReader(ABC):
    @abstractmethod
    def read_bet_amount(self) -> int:
        pass