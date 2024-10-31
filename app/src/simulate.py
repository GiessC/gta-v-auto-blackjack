from analytics.analytics import Analytics
from analytics.result.win_result import WinResult
from blackjack.player.basic_strategy_player import BasicStrategyPlayer
from blackjack.settings.blackjack_settings import BlackjackSettings
from blackjack.table.table import Table
from blackjack.table.table_state import TableState


def simulate():
    chip_count = 100_000
    settings = BlackjackSettings(stop_at_loss_gte=100_000, bet_amount=50_000)
    settings._simulate = True
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
    simulate()
