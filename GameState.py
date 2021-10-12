from __future__ import annotations

from collections import defaultdict
from CharacterManager import CharacterManager
from DialogueManager import DialogueManager
from RoomManager import RoomManager

event_callbacks = defaultdict(list)
room_manager = RoomManager()
character_manager = CharacterManager()
dialogue_manager = DialogueManager()


def register(event_type, observer):
    event_callbacks[event_type].append(observer)


def publish(event_type, message):
    for observer in event_callbacks[event_type]:
        observer.listener_event(message)
