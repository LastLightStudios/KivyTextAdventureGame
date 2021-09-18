from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self, client) -> None:
        pass


class TravelCommand(Command):

    def __init__(self, room_map, direction="forgot to give direction"):
        self._room_map = room_map
        self._direction = direction

    def execute(self, client) -> None:
        self._room_map.travel(self._direction, client.enter_room)


class InteractCommand(Command):

    def __init__(self, root_container=None):
        self._root_container = root_container
        pass

    def execute(self, client) -> None:
        print("Interact")
