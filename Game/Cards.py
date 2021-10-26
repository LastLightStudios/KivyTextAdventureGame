from __future__ import annotations

from abc import ABC, abstractmethod
from Game.Commands import Command


class Card(Command):
    """
    The Card interface looks like a Command Interface, except execute returns a boolean instead of None.
    Card is being used instead of "Move" because it isn't clear "Move" is a noun rather than an verb.
    A Card is a "Move" taken during Combat that may cause a cascade of Actions(TBD) afterwards

    def __init__(self, *args):
    *args will be passed in from the Character. The Character creates the Card.

    def execute(self) -> bool:
    Execute "plays" the "card" or executes the Move
    """

    def __init__(self, game_state):
        self.game_state = game_state

    def execute(self) -> None:
        self.game_state.combat_manager.process_turn(self)

    @abstractmethod
    def process(self) -> bool:
        pass


class PassCard(Card):
    def __init__(self, game_state, character):
        self.game_state = game_state
        self.character = character
        pass

    def process(self) -> bool:
        self.game_state.publish("Log", {"Log": self.character.name + " passes", "Clear": False})
        return True


class TempWinCard(Card):
    """This does not follow the paradigm and is going to bypass normal WinCond"""

    def __init__(self, game_state):
        self.game_state = game_state

    def process(self) -> bool:
        return self.game_state.combat_manager.just_win_fourhead()
