from __future__ import annotations

from abc import ABC, abstractmethod
from Game.Commands import Command


class TargetingAction(Command):
    """
    The TargetingAction Interface is a way to add the targets to the Card to resolve.
    """

    def __init__(self, game_state):
        self.game_state = game_state


    """
    Execute() is triggered either by the button press or the AI.
    In the case of the Button press, there can be multiple variants of the action.
    Ex:
    A single target damage action will have the same process() method of:
    Deal damage from Source to Target.
    But the buttons will have actions that are initialized with different targets.
    
    An AoE may have a list of targets instead
    
    """

    def execute(self) -> None:
        self.game_state.combat_manager.process_turn(self)

class SingleTargetAction(TargetingAction):

    def __init__(self, game_state, card, target):
        self.game_state = game_state
        self.card = card
        self.target = target

    def execute(self) -> None:
        self.card.process(self.target)

