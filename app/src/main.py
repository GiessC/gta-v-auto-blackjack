import pytesseract

from analytics.analytics import Analytics
from analytics.result.win_result import WinResult
from blackjack.player.basic_strategy_player import BasicStrategyPlayer
from blackjack.settings.blackjack_settings import BlackjackSettings, ChipReadMethod
from blackjack.table.table import Table
from blackjack.table.table_state import TableState
from read.bet_reader.positional_bet_reader import PositionalBetReader
from read.chip_reader.experimental_ocr_chip_reader import ExperimentalOCRChipReader
from read.chip_reader.input_chip_reader import InputChipReader
from read.help_reader.positional_help_reader import HelpReader
from read.settings.ocr_settings import OCRSettings

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Collin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def main():
    settings = BlackjackSettings()
    chip_reader = None
    if settings.chip_read_method == ChipReadMethod._EXPERIMENTAL_OCR:
        chip_reader = ExperimentalOCRChipReader()
    elif settings.chip_read_method == ChipReadMethod.INPUT:
        chip_reader = InputChipReader()
    else:
        raise ValueError("Invalid chip read method")
    chip_count = chip_reader.read_chips()
    stop_at_loss_gte = input("How much money are you willing to lose? If you have lost more than this amount, the program will stop. $")
    bet_amount = input("How much would you like to bet each hand? $")
    settings.stop_at_loss_gte = int(stop_at_loss_gte)
    settings.bet_amount = int(bet_amount)
    player = BasicStrategyPlayer(settings, chip_count)
    analytics = Analytics(player)

    table = Table(settings, player)

    while player.chip_count >= settings.bet_amount and analytics.profit() > -settings.stop_at_loss_greater_than:
        table.print_info()
        player.place_bet(settings.bet_amount)
        table.print_info()

        player.play_hands(table.get_dealer_upcard())
        table.print_info()

        if table.state == TableState.DEALER_TURN:
            table.simulate_dealer_turn()

        table.print_info()
        results = table.determine_hand_results()

        for result in results:
            if isinstance(result, WinResult):
                player.add_chips((result.bet * result.multiplier) + result.bet)

        analytics.track_results(results)
        print(analytics)

        table.reset()

if __name__ == "__main__":
    main()
