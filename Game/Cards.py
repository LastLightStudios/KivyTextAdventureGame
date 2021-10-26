from __future__ import annotations

from abc import ABC, abstractmethod
from Game.Commands import Command
import Game.BattleAction as BA


class Card(Command):
    """
    The Card interface inherits from the Command Interface so that the buttons can call them.
    Cards have an additional layer where they will create more Commands, called Targeting Actions.
    """

    def __init__(self, game_state):
        self.game_state = game_state

    """
    def execute(self) -> None:
        this will create targeting actions
        temp: if source.name == "Player" then publish
        else
        process("Player"), which means it'll target the player, but we don't have the enemy attacking yet so it doesnt matter
        
        In the case of automatically self-targeted Card, it'll immediately call self.process()
    """

    @abstractmethod
    def execute(self) -> None:
        pass

    """
    This is overridden in the case there it is not an automatically self-targeted Card.
    This is what the targeting action will call, passing in the relevant targets.
    if its a single target attack, then process will only expect one target.
    in an AoE, it'll accept a list, instead.
    
    this will modify the Cards targets, which was None
    It then tells the combat manager it's ready to be called
    """
    def process(self) -> None:
        self.game_state.combat_manager.process_turn(self)

    """
    This is called by the combat manager. This resolves the actual action on the targets.
    It should then return True to let the CombatManager it completed. If it is to return False, then somethign went wrong.
    I will create a bug report if it returns false. something like "X char performing Y action targeting Z actors failed"
    """
    @abstractmethod
    def perform(self) -> bool:
        pass



class TempDealDMGCard(Card):
    def __init__(self, game_state, source):
        self.game_state = game_state
        self.source = source
        self.target = None

    def execute(self) -> None:
        command_dict = {}
        for enemy in self.game_state.combat_manager.get_enemy_list():
            command_dict[enemy.name] = BA.SingleTargetAction(self.game_state, self, enemy)
        self.game_state.publish("Commands", {"Commands": command_dict})
        self.game_state.publish("Log", {"Log": "Select Target", "Clear": False})


    def process(self, single_target) -> None:
        self.target = single_target
        self.game_state.combat_manager.process_turn(self)

    def perform(self) -> bool:
        self.game_state.publish("Log", {"Log": self.source.name +
                                               " attacks " + self.target.name, "Clear": False})
        return True


class PassCard(Card):
    def __init__(self, game_state, character):
        self.game_state = game_state
        self.character = character

    def execute(self) -> None:
        self.process()

    def perform(self) -> bool:
        self.game_state.publish("Log", {"Log": self.character.name + " passes", "Clear": False})
        return True


class TempWinCard(Card):
    """This does not follow the paradigm and is going to bypass normal WinCond"""

    def __init__(self, game_state):
        self.game_state = game_state

    def execute(self) -> None:
        self.process()

    def perform(self) -> bool:
        return self.game_state.combat_manager.just_win_fourhead()
