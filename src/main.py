import pytesseract

from blackjack.settings.settings import Settings
from blackjack.player.basic_strategy_player import BasicStrategyPlayer
from blackjack.card.card import Card
from blackjack.card.card_factory import CardFactory
from ocr.image_reader import ImageReader
from ocr.areas.blackjack_areas import Areas

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Collin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


class Scenario:
    player_cards: list[Card]
    dealer_card: Card

    def __init__(self, player_cards: list[Card], dealer_card: Card):
        self.player_cards = player_cards
        self.dealer_card = dealer_card


image_reader = ImageReader()

def main():
    scenario: Scenario = Scenario([
        CardFactory.create_ace(),
        CardFactory.create_four(),
        CardFactory.create_three(),
    ], CardFactory.create_seven())
    settings = Settings()
    bet_amount = 50_000
    start_amount = 200_000
    player = BasicStrategyPlayer(settings, bet_amount, start_amount)

    read_chips()


def read_chips():
    image_path = 'src/resources/img/betting.png'
    text = image_reader.read_image(image_path, Areas.Chips)
    print(text)


if __name__ == "__main__":
    main()
