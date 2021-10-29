from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque

import Game.GameState as GameState
from Game.Commands import EnterCurrentRoomCommand

"""
turn order
end conditions
"""

@dataclass
class CombatManager:
    init_queue: deque = deque()
    init_list: list = field(default_factory=list)
    initiative_tracker: int = 0
    is_won: bool = False
    player_party: list = field(default_factory=list)
    enemy_party: list = field(default_factory=list)

    """this is a temp, and needs to be replaced with an intelligent version that cares about sides"""
    def get_enemy_list(self):
        return self.enemy_party

    def enter_combat_with(self, enemy_list):
        self.is_won = False
        """clear commands"""
        """ queries for characters in encounter """
        """ """
        self.init_queue.clear()
        self.init_list.clear()
        self.init_list.append(GameState.character_manager.character_dict["Player"])
        self.init_queue.append(GameState.character_manager.character_dict["Player"])
        initiative_string = "\n Initiative: "
        for enemy in enemy_list:
            self.init_list.append(enemy)
            self.init_queue.append(enemy)
            self.enemy_party.append(enemy)

        for character in self.init_queue:
            initiative_string += character.name + ", "
        GameState.publish("Log", {"Log": initiative_string, "Clear": False})

        """
        takes enemy list
        GameState.publish("Enter Combat", {"Enemies": enemy_list})
        this line triggers the right panel to create the combat panel
        """
        GameState.publish("Enter Combat", {"Enemies": enemy_list})
        self.take_turn()

    def just_win_fourhead(self):
        self.is_won = True
        return True

    def take_turn(self):
        """
        calls take_turn() on first in queue
        for user this will publish commands
        for AI this will call execute on a Card - which just calls process turn, passing itself in
        """
        print(self.init_list[self.initiative_tracker].name + " is taking a turn")
        self.init_list[self.initiative_tracker].take_turn()
        pass

    def process_turn(self, command):
        """
        this is where the command is executed on
        if it executes successfully it will go to complete_turn()
        if not it'll return back to take_turn
        in normal gameplay, I don't think it'll ever go back to take_turn()
        if an attack fizzles b/c of immunity or some other reason, then it'll still consume the turn
        """
        if command.perform() is True:
            self.complete_turn()
        else:
            self.take_turn()

    def complete_turn(self):
        """
        this will check WinCond
        this is called when the turn is completed and will enqueue the first and then pop it
        """
        if all((enemy.health <= 0) for enemy in self.enemy_party):
            self.is_won = True

        if self.is_won is True:
            GameState.publish("Log", {"Log": "You have won!", "Clear": False})
            GameState.publish("Commands", {"Commands": {"Return": EnterCurrentRoomCommand(GameState)}})
        else:
            self.init_queue.append(self.init_queue[0])
            self.init_queue.popleft()
            self.initiative_tracker += 1
            if self.initiative_tracker >= len(self.init_list):
                self.initiative_tracker -= len(self.init_list)
            self.take_turn()
