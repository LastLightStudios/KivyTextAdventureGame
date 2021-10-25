from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    """
    The Command interface declares a method for executing a command.

    def __init__(self, *args):
    *args will be passed in from the Model. The Model creates the command.

    def execute(self, client) -> None:
    client is a callback to pass the information to the View
    execute should call something like
    manager.function(*args, client.callback)
    """

    @abstractmethod
    def execute(self) -> None:
        pass


class OneVsOneFightCommand(Command):

    def __init__(self, game_state, enemy):
        self.game_state = game_state
        self.enemy = enemy

    def execute(self) -> None:
        self.game_state.combat_manager.enter_combat_with(self.enemy)


class TempChangeHPCommand(Command):

    def __init__(self, character, amount):
        self.character = character
        self.amount = amount

    def execute(self) -> None:
        self.character.modify_health(self.amount)


class TempChangePhaseCommand(Command):

    def __init__(self, game_state, game_phase):
        self.game_state = game_state
        self.game_phase = game_phase

    def execute(self) -> None:
        self.game_state.change_game_phase(self.game_phase)


# used on exiting a dialogue tree
class EnterCurrentRoomCommand(Command):

    def __init__(self, game_state):
        self.game_state = game_state

    def execute(self) -> None:
        self.game_state.room_manager.room_map.enter_current_room()


class InteractCommand(Command):

    def __init__(self, game_state, character):
        self.game_state = game_state
        self.character = character

    def execute(self) -> None:
        self.game_state.character_manager.interact_with_character(self.character)


class DirectDialogueCommand(Command):

    def __init__(self, story, link_path):
        self.story = story
        self.link_path = link_path

    def execute(self) -> None:
        print("Executing to linkpath" + self.link_path)
        self.story.build_node(self.link_path)

# TODO story stuff
class AddFlagDialogueCommand(Command):

    def __init__(self, link_path):
        self.link_path = link_path

    def execute(self) -> None:
        # will look like direct dialogue command but additionally add a flag wherever
        pass


class TravelCommand(Command):

    def __init__(self, room_map, direction="forgot to give direction"):
        self._room_map = room_map
        self._direction = direction

    def execute(self) -> None:
        self._room_map.travel(self._direction)
