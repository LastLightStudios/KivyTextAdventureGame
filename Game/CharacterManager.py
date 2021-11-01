from __future__ import annotations

import jsonpickle
from dataclasses import dataclass, field
from pathlib import Path
from Game.Commands import EnterCurrentRoomCommand, OneVsOneFightCommand, OneVsManyFightCommand
from Game.Cards import PassCard, TempWinCard, TempDealDMGCard
import Game.GameState as GameState


@dataclass
class Character(object):
    name: str = ""
    health: int = 90
    max_health: int = 100
    second_health: int = 50
    intro_text: str = ""
    dialogue_options_list: list = field(default_factory=list)
    command_list: dict = field(default_factory=dict)

    def is_dead(self):
        if self.health <= 0:
            return True
        else:
            return False

    def get_intro_text(self):
        return self.intro_text

    def modify_health(self, amount):
        log = "Health Changed"
        self.health += amount
        if self.health <= 0 and amount < 0:
            log = self.name + " is already dead!"
        elif self.health > self.max_health:
            log = "You look bloated."
        GameState.publish("Health Change", {self.name: self.health})
        GameState.publish("Log", {"Log": log, "Clear": False})

    def get_character_command_dict(self):
        command_dict = {"Back": EnterCurrentRoomCommand(GameState)}
        """temp commenting out the story stuff so we can add characters easily for now"""
        """file_path = Path("Dialogue/" + self.name + "Test.txt")
        GameState.dialogue_manager.load_story(file_path)
        command_dict.update(GameState.dialogue_manager.story.get_story_commands())"""
        command_dict.update({"Fight": OneVsOneFightCommand(GameState, [self.name])})
        command_dict.update({"Fight Room": OneVsManyFightCommand(GameState, GameState.room_manager.room_map.current_room.get_character_names())})
        # add fight here?
        # for string in self.dialogue_options_list:
        return command_dict

    def get_temp_dict(self):
        command_dict = {"Back": EnterCurrentRoomCommand(GameState)}
        ## will add battle commands
        return command_dict

    def take_turn(self):
        if self.name == "Player":
            GameState.publish("Commands", {"Commands": self.get_temp_pc_attacks()})
        else:
            PassCard(GameState, self).execute()

    def get_temp_pc_attacks(self):
        command_dict = {"Pass": PassCard(GameState, self),
                        "Attack": TempDealDMGCard(GameState, self),
                        "Win": TempWinCard(GameState)}
        return command_dict

    #"Attack": TempDealDMGCard(GameState, self, GameState.character_manager.character_dict["Joanna"])

    def get_temp_npc_attacks(self):
        command_dict = {"Pass": PassCard(GameState, self)}
        return command_dict


@dataclass()
class CharacterManager:
    character_dict: dict = field(default_factory=dict)
    """ I don't know if this \/ is staying """
    player_party_dict: dict = field(default_factory=dict)

    def __post_init__(self):
        self.character_dict = {"Player": Character(name="Player")}
        self.player_party_dict = {"Player": Character(name="Player")}

    def load(self, file_path):
        with open(file_path, "r") as load_file:
            frozen = load_file.read()
            char_info = jsonpickle.decode(frozen)
            for key, value in char_info:
                self.character_dict[key] = value

    def save(self, file_path):
        char_info = jsonpickle.encode(self.character_dict, indent=4, keys=True)
        with open(file_path, "w") as save_file:
            save_file.write(char_info)

    def interact_with_character(self, character):
        GameState.publish("Commands", {"Commands": character.get_character_command_dict()})
        GameState.publish("Log", {"Log": "Interacting with " + character.name, "Clear": True})
        # temporarily excluding story part for now
        # GameState.publish("Log", {"Log": GameState.dialogue_manager.story.get_story_log(), "Clear": True})
