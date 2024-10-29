from enum import Enum


class ActionType(Enum):
    HIT = 'HIT'
    STAND = 'STAND'
    DOUBLE = 'DOUBLE'
    SPLIT = 'SPLIT'

class Action:
    action_type: ActionType

    def __init__(self, primary_action: ActionType, secondary_action: ActionType | None = None, should_use_primary: bool = True):
        if should_use_primary:
            self.action_type = primary_action
            return
        self.action_type = secondary_action
