from __future__ import annotations

from dataclasses import dataclass, field

import Game.GameState as GameState

@dataclass
class CombatManager:
    initiative_order: list = field(default_factory=list)

    def enter_combat_with(self, enemy_list):
        GameState.publish("Enter Combat", {"Enemies": enemy_list})

    def win_combat(self):
        # shows log
        # adds enter current room button
        pass


