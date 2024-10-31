from blackjack.player.basic_strategy_player import BasicStrategyPlayer
from blackjack.settings.blackjack_settings import BlackjackSettings
from blackjack.table.table import Table
from blackjack.table.table_state import TableState


def simulate():
    chip_count = 100_000
    settings = BlackjackSettings(bet_amount=50_000)
    settings.test = True
    player = BasicStrategyPlayer(settings, chip_count)

    table = Table(settings, player)

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
        print(result)

if __name__ == "__main__":
    simulate()
