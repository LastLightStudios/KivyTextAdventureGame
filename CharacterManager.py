from __future__ import annotations

import jsonpickle
from dataclasses import dataclass, field
from pathlib import Path
import DialogueManager
from Commands import EnterCurrentRoomCommand


@dataclass
class Character(object):
    name: str = ""
    health: int = 50
    max_health: int = 100
    second_health: int = 50
    intro_text: str = ""
    dialogue_options_list: list = field(default_factory=list)
    command_list: dict = field(default_factory=dict)

    def get_intro_text(self):
        return self.intro_text

    def get_stats(self):
        return {"Health": self.health, "Max Health": self.max_health}

    def modify_health(self, amount, client_callback):
        log = ""
        self.health += amount
        if self.health <= 0 and amount < 0:
            log = "Stop, you're already dead!"
        elif self.health > self.max_health:
            log = "You look bloated."
        client_callback({"Current Health": self.health, "Log": log})

    def get_character_command_dict(self):
        command_dict = {"Back": EnterCurrentRoomCommand()}
        file_path = Path("Dialogue/" + self.name + "Test.txt")
        DialogueManager.load_story(file_path)
        command_dict.update(DialogueManager.story.get_story_commands())
        # for string in self.dialogue_options_list:
        return command_dict


@dataclass()
class CharacterManager:
    character_dict: dict = field(default_factory={"Player": Character(name="Player")})

    def load(file_path):
        with open(file_path, "r") as load_file:
            frozen = load_file.read()
            char_info = jsonpickle.decode(frozen)
            for key, value in char_info:
                character_dict[key] = value

    def save(file_path):
        char_info = jsonpickle.encode(character_dict, indent=4, keys=True)
        with open(file_path, "w") as save_file:
            save_file.write(char_info)

    def interact_with_character(character, client_callback):
        client_callback({"Commands": character.get_character_command_dict(),
                         "Log": DialogueManager.story.get_story_log()})
