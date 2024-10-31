from abc import ABC, abstractmethod
from read.image.image_reader import ImageReader
from read.settings.ocr_settings import OCRSettings


class HelpReader(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read_help_msg(self) -> int:
        pass

    @abstractmethod
    def read_for_card_total(self) -> int:
        pass