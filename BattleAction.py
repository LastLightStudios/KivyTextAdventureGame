from abc import ABC, abstractmethod


class BattleAction(ABC):
    """

    """

    @abstractmethod
    def execute(self, source, target) -> None:
        pass

class LoseHPAction(BattleAction):

    def __init__(self):
        self.HP_loss = 10

    # expecting source and target to be the same
    def execute(self, source, target) -> None:
        pass