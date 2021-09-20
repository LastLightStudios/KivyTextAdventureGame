from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self, client) -> None:
        pass


class EnterCurrentRoomCommand(Command):

    def execute(self, client) -> None:
        client.enter_current_room()


class InteractCommand(Command):

    def __init__(self, character):
        self.character = character

    def execute(self, client) -> None:
        client.interact_with_character(self.character)


class DirectDialogueCommand(Command):

    def __init__(self, story, link_path):
        self.story = story
        self.link_path = link_path

    def execute(self, client) -> None:
        self.story.build_node(self.link_path, client.dialogue_pressed)


class AddFlagDialogueCommand(Command):

    def __init__(self, link_path):
        self.link_path = link_path

    def execute(self, client) -> None:
        # will look like direct dialogue command but additionally add a flag wherever
        pass


class TravelCommand(Command):

    def __init__(self, room_map, direction="forgot to give direction"):
        self._room_map = room_map
        self._direction = direction

    def execute(self, client) -> None:
        self._room_map.travel(self._direction, client.enter_room)
