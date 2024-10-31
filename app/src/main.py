import time
import pytesseract

from analytics.counters.profit_counter import ProfitCounter
from blackjack.settings.blackjack_settings import BlackjackSettings, ChipReadMethod
from blackjack.player.basic_strategy_player import BasicStrategyPlayer
from blackjack.table.table import Table
from read.chip_reader.experimental_ocr_chip_reader import ExperimentalOCRChipReader
from read.chip_reader.input_chip_reader import InputChipReader
from read.settings.ocr_settings import OCRSettings

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Collin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def main():
    blackjack_settings = BlackjackSettings()

    ocr_settings = OCRSettings(debug=True)
    chip_reader = None
    if blackjack_settings.chip_read_method == ChipReadMethod.INPUT:
        chip_reader = InputChipReader()
    elif blackjack_settings.chip_read_method == ChipReadMethod.__EXPERIMENTAL_OCR:
        chip_reader = ExperimentalOCRChipReader(ocr_settings)

    start_amount = chip_reader.read_chips()
    bet_amount = int(input(f'You have {start_amount} chips. How much would you like to bet each round? $'))

    player = BasicStrategyPlayer(blackjack_settings, start_amount)
    profit_counter = ProfitCounter(player)
    table = Table(player)

    player.play(bet_amount, table.get_dealer_upcard())
    print('Profit', profit_counter.count())


if __name__ == "__main__":
    main()
