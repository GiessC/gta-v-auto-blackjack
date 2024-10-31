class PlayerObserver:
    def on_bet_placed(self, player, amount: int):
        pass

    def on_win(self, player, amount: int):
        pass

    def on_hands_played(self, player):
        pass
