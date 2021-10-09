import jsonpickle
from dataclasses import dataclass, field
from pathlib import Path
import DialogueManager
from Commands import EnterCurrentRoomCommand

character_dict = {}


def load(file_path):
    global character_dict
    with open(file_path, "r") as load_file:
        frozen = load_file.read()
        char_info = jsonpickle.decode(frozen)
        for key, value in char_info:
            character_dict[key] = value


def save(file_path):
    global character_dict
    char_info = jsonpickle.encode(character_dict, indent=4, keys=True)
    with open(file_path, "w") as save_file:
        save_file.write(char_info)



def interact_with_character(character, client_callback):
    client_callback({"Commands": character.get_character_command_dict(),
                     "Log": DialogueManager.story.get_story_log()})


@dataclass
class Character(object):
    name: str = ""
    health: int = 50
    second_health: int = 50
    intro_text: str = ""
    dialogue_options_list: list = field(default_factory=list)
    command_list: dict = field(default_factory=dict)

    def get_intro_text(self):
        return self.intro_text

    def get_character_command_dict(self):
        command_dict = {"Back": EnterCurrentRoomCommand()}
        file_path = Path("Dialogue/" + self.name + "Test.txt")
        DialogueManager.load_story(file_path)
        command_dict.update(DialogueManager.story.get_story_commands())
        # for string in self.dialogue_options_list:
        return command_dict
