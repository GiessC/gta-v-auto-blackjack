from enum import Enum

class TableState(Enum):
    BETTING = 0
    DEALING = 1
    PLAYER_TURN = 2
    DEALER_TURN = 3
    COMPLETE = 4