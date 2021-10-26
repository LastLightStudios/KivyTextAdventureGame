from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque

import Game.GameState as GameState

"""
turn order
end conditions
"""

@dataclass
class CombatManager:
    init_queue: deque = deque()

    def enter_combat_with(self, enemy_list):
        """clear commands"""
        """ queries for characters in encounter """
        """ """
        self.create_init_order()
        self.init_queue.clear()
        self.init_queue.append(GameState.character_manager.character_dict["Player"])
        initiative_string = "\n Initiative: "
        for enemy in enemy_list:
            self.init_queue.append(enemy)

        for character in self.init_queue:
            initiative_string += character.name + ", "
        GameState.publish("Log", {"Log": initiative_string, "Clear": False})

        """
        takes enemy list
        GameState.publish("Enter Combat", {"Enemies": enemy_list})
        this line triggers the right panel to create the combat panel
        """
        GameState.publish("Enter Combat", {"Enemies": enemy_list})

    def take_turn(self):
        """
        https://www.geeksforgeeks.org/queue-in-python/
        initiative_order[0].taketurn()
        taketurn() on the character will publish commands/actions
        """
        pass

    def complete_turn(self):
        """
        this is called when the turn is completed and will enqueue
        """

    def create_init_order(self):
        #
        pass

    def win_combat(self):
        # shows log
        # adds enter current room button
        pass


