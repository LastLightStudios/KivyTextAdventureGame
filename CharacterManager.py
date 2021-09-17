import jsonpickle
from dataclasses import dataclass, field


@dataclass
class CharacterManager(object):
    character_dict: dict = field(default_factory=dict)

    def load_file(self, file_path):
        with open(file_path, "r") as load_file:
            frozen = load_file.read()
            char_info = jsonpickle.decode(frozen)
            for key, value in char_info:
                self.character_dict[key] = value

    def save(self, file_path):
        char_info = jsonpickle.encode(self.character_dict, indent=4, keys=True)
        with open(file_path, "w") as save_file:
            save_file.write(char_info)


@dataclass
class Character(object):
    name: str = ""
    health: int = 50
    second_health: int = 50
    intro_text: str = ""
    command_list: dict = field(default_factory=dict)
