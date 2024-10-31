from blackjack.table.table_state import TableState


class TableObserver:
    def on_state_change(self, state: TableState, table):
        pass
