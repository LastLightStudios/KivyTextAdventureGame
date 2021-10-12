from __future__ import annotations


from collections import defaultdict
from CharacterManager import CharacterManager

event_callbacks = defaultdict(default_factory=list)
character_manager = CharacterManager()


def register(event_type, observer):
    event_callbacks[event_type].append(observer)


def publish(event_type, message):
    for observer in event_callbacks[event_type]:
        observer.event_callback(message)
