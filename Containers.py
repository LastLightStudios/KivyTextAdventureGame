import kivy

kivy.require('2.0.0')
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from StatDisplay import CharacterStatBlockDisplay  # surprised i dont need to import the context menu?
from KivyOtherCharacterManager import KivyCharacterManager

import GameState
import RoomManager
import DialogueManager
from CharacterManager import Character
from Commands import DirectDialogueCommand, EnterCurrentRoomCommand, InteractCommand, TravelCommand, TempChangeHPCommand


class LeftPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(LeftPanelWidget, self).__init__(**kwargs)

    def init_complete(self):
        pass


class RightPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(RightPanelWidget, self).__init__(**kwargs)

    def init_complete(self):
        pass


class CenterPanelWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CenterPanelWidget, self).__init__(**kwargs)


class GameContainer(BoxLayout):
    left_panel = ObjectProperty()
    right_panel = ObjectProperty()
    scrollable_widget = ObjectProperty()
    grid_manager = ObjectProperty()
    character_display = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameContainer, self).__init__(**kwargs)
        self.room_manager = GameState.room_manager
        self.room_manager.load(r"Maps\NewFile2.txt")
        # need to load in characters before room, b/c room has Interact which needs chara ref
        GameState.character_manager.character_dict["Joanna"] = Character(name="Joanna", intro_text="I'm Joanna, how are you?")
        GameState.character_manager.character_dict["Steve"] = Character(name="Steve", intro_text="Sup, I'm Steve")
        GameState.character_manager.character_dict["Joe"] = Character(name="Steve", intro_text="It's Joe")
        GameState.character_manager.character_dict["Mama"] = Character(name="Steve", intro_text="And I'm Mama")
        self.enter_current_room()
        self.temp_set_hp(GameState.character_manager.character_dict["Player"].get_stats()["Health"],
                         GameState.character_manager.character_dict["Player"].get_stats()["Max Health"])
        # this one probably gets moved down to the scrollable widget - which is currently sitting in main
        GameState.register("Log", self)
        # this one probably gets moved down to commands later
        GameState.register("Commands", self)

    def listener_event(self, info):
        if "Log" in info:
            if "Clear" in info:
                if info["Clear"]:
                    self.scrollable_widget.replace_text(info["Log"])
                else:
                    self.scrollable_widget.add_text(info["Log"])
            else:
                print("Need to add clear to this Log in info")
        if "Commands" in info:
            self.update_context_menu(info["Commands"])

    # Accepts a dict of info to update the screen
    def update_view_info(self, info):
        if "Commands" in info:
            self.update_context_menu(info["Commands"])
        if "Log" in info:
            self.update_log(info["Log"])

    # only used on setup for now
    def temp_set_hp(self, current_hp, max_hp):
        self.character_display.update_health(current_hp, max_hp)

    def enter_current_room(self):
        self.update_view_info({"Commands": self.room_manager.room_map.current_room.get_room_command_dict(),
                               "Log": self.room_manager.room_map.current_room.get_room_desc()})

    def update_log(self, new_text):
        self.scrollable_widget.replace_text(new_text)

    def update_context_menu(self, command_dict):
        self.grid_manager.clear_buttons()
        top_row_iter = 0
        self.grid_manager.button_list[9].set_command(TempChangeHPCommand(GameState.character_manager.character_dict["Player"], 10))
        self.grid_manager.button_list[9].set_display_text("hpmod+")
        self.grid_manager.button_list[4].set_command(
            TempChangeHPCommand(GameState.character_manager.character_dict["Player"], -10))
        self.grid_manager.button_list[4].set_display_text("hpmod-")
        for key, command in command_dict.items():
            if isinstance(command, InteractCommand):
                pass
                """
                if self.grid_manager.button_list[top_row_iter].has_command():
                    top_row_iter += 1
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
                else:
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
                """
            elif isinstance(command, TravelCommand):
                self.grid_manager.button_list[self.convert_dir_to_button(key)].set_command(command)
                self.grid_manager.button_list[self.convert_dir_to_button(key)].set_display_text(key)
            elif isinstance(command, DirectDialogueCommand):
                if self.grid_manager.button_list[top_row_iter].has_command():
                    top_row_iter += 1
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
                else:
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
            elif isinstance(command, EnterCurrentRoomCommand):
                self.grid_manager.set_button_command_and_text(14, key, command)
            else:
                print("Unhandled Command")

    @staticmethod
    def convert_dir_to_button(direction):
        switcher = {
            "Forward": 6,
            "Forwards": 6,
            "Left": 10,
            "Backward": 11,
            "Backwards": 11,
            "Right": 12
        }
        return switcher.get(direction)
