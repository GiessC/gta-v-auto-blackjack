from blackjack.player.pub_sub.player_hand_observer import PlayerHandObserver


class WinLossCounter(PlayerHandObserver):
    wins: int
    losses: int

    def __init__(self):
        self.wins = 0
        self.losses = 0

    def on_win(self, player, hand):
        self.wins += 1

    def on_loss(self, player, hand):
        self.losses += 1

    def get_percentage(self) -> float:
        total = self.wins + self.losses
        if total == 0:
            return 0
        return self.wins / total
