import time
from typing import List, Tuple
from analytics.result.dealer_blackjack_result import DealerBlackjackResult
from analytics.result.dealer_bust_result import DealerBustResult
from analytics.result.loss_result import LossResult
from analytics.result.player_blackjack_result import PlayerBlackjackResult
from analytics.result.player_bust_result import PlayerBustResult
from analytics.result.push_result import PushResult
from analytics.result.result import Result
from analytics.result.win_result import WinResult
from blackjack.card.card import Card
from blackjack.card.card_factory import CardFactory
from blackjack.exceptions.invalid_state_exception import InvalidStateException
from blackjack.player.player import Player
from blackjack.player.player_hand import PlayerHand
from blackjack.player.pub_sub.player_hand_observer import PlayerHandObserver
from blackjack.player.pub_sub.player_observer import PlayerObserver
from blackjack.settings.blackjack_settings import BlackjackSettings
from blackjack.table.table_state import TableState
from read.image.image_finder import ImageFinder


class Table(ImageFinder, PlayerObserver, PlayerHandObserver):
    settings: BlackjackSettings
    state: TableState
    player: Player
    dealer_hand: PlayerHand

    def __init__(self, settings: BlackjackSettings, player: Player, state: TableState = TableState.BETTING):
        super().__init__()

        self.settings = settings
        self.state = state
        self.player = player
        self.player.attach(self)
        self.dealer_hand = PlayerHand(0)
        self.dealer_hand.attach(self)

    def determine_hand_results(self) -> List[Result]:
        results: List[Result] = []

        for hand in self.player.hands:
            if hand.is_bust():
                results.append(PlayerBustResult(hand.total, self.dealer_hand.total))
            elif hand.total == self.dealer_hand.total:
                results.append(PushResult(hand.total))
            elif hand.is_blackjack():
                results.append(PlayerBlackjackResult(self.dealer_hand.total))
            elif self.dealer_hand.is_blackjack():
                results.append(DealerBlackjackResult(hand.total))
            elif self.dealer_hand.is_bust():
                results.append(DealerBustResult(hand.total, self.dealer_hand.total))
            elif hand.total > self.dealer_hand.total:
                results.append(WinResult(hand.total, self.dealer_hand.total))
            else:
                results.append(LossResult(hand.total, self.dealer_hand.total))
        return results

    def get_dealer_upcard(self) -> Card | None:
        if len(self.dealer_hand.cards) == 0:
            return None
        return self.dealer_hand.cards[0]

    def on_bet_placed(self, player: Player, amount: int):
        print(f'{player.name} placed bet of ${amount}.')
        if (self.state != TableState.BETTING):
            raise InvalidStateException(f'Cannot place bet when state is {self.state}')

        self.state = TableState.DEALING
        print()
        print(f'Dealer is dealing cards... Polling for player turn.')
        self.poll_for_player_turn()
        self.state = TableState.PLAYER_TURN
        print(f'Started player turn.')

    def on_hands_played(self, player):
        print()
        print(f'{player.name} has played all hands.')
        if (self.did_player_bust_all()):
            self.state = TableState.COMPLETE
            print('Player has bust all hands. Game is complete.')
            return
        self.state = TableState.DEALER_TURN
        print('Dealer is playing...')

    def on_card_added(self, dealer_hand: PlayerHand, card: Card):
        if dealer_hand.stood or dealer_hand.is_bust():
            self.state = TableState.COMPLETE
            print('Dealer has played. Game is complete.')

    def find_time_text(self) -> Tuple[int, int, int, int] | None:
        time_text_path = 'app/src/resources/img/time_text.png'
        return self.find_image(time_text_path)

    def did_player_bust_all(self) -> bool:
        for hand in self.player.hands:
            if not hand.is_bust():
                return False
        return True

    def check_player_turn(self) -> bool:
        loc = self.find_time_text()
        return loc is not None

    def poll_for_player_turn(self):
        if self.settings.test:
            self.simulate_dealing()
            return
        max_tries = 10
        tries = 1
        poll_interval_seconds = 3
        finished_dealing = self.check_player_turn()
        while not finished_dealing and tries < max_tries:
            time.sleep(poll_interval_seconds)
            finished_dealing = self.check_player_turn()
            tries += 1
        if not finished_dealing:
            raise InvalidStateException(f'Timed out ({max_tries * poll_interval_seconds} sec.) while polling for player turn. Exiting...')

    def simulate_dealing(self):
        self.state = TableState.DEALING
        hand = PlayerHand(self.settings.bet_amount)
        hand.add_card(CardFactory.create_two())
        self.dealer_hand.add_card(CardFactory.create_ten())
        hand.add_card(CardFactory.create_six())
        self.player.hands.append(hand)

    def simulate_dealer_turn(self):
        self.state = TableState.DEALER_TURN
        while self.dealer_hand.total < 17:
            card = CardFactory.random()
            print(f'Dealer total: {self.dealer_hand.total}. Dealer hits {card}.')
            self.dealer_hand.add_card(card)
        if self.dealer_hand.total > 21:
            print(f'Dealer total: {self.dealer_hand.total}. Dealer busts.')
        else:
            print(f'Dealer total: {self.dealer_hand.total}. Dealer stands.')
        self.state = TableState.COMPLETE

    def print_info(self):
        print()
        print(self.state)
        if self.state == TableState.BETTING:
            print()
            return
        print('Player Cards:', self.player.hands_to_string())
        print('Dealer Cards:', str(self.dealer_hand))
        print()
