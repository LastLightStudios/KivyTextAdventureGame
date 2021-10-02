import kivy
kivy.require('2.0.0')
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from StatDisplay import CharacterStatBlockDisplay # surprised i dont need to import the context menu?

import RoomManager
import CharacterManager
import DialogueManager
from CharacterManager import Character
from Commands import DirectDialogueCommand, EnterCurrentRoomCommand, InteractCommand, TravelCommand


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

    def init_complete(self):
        for child in self.children:
            child.init_complete()


class GameContainer(BoxLayout):
    left_panel = ObjectProperty()
    right_panel = ObjectProperty()
    scrollable_widget = ObjectProperty()
    grid_manager = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameContainer, self).__init__(**kwargs)
        self.room_manager = RoomManager
        self.room_manager.load(r"Maps\NewFile2.txt")
        # need to load in characters before room, b/c room has Interact which needs chara ref
        CharacterManager.character_dict["Joanna"] = Character(name="Joanna", intro_text="I'm Joanna, how are you?")
        CharacterManager.character_dict["Steve"] = Character(name="Steve", intro_text="Sup, I'm Steve")
        CharacterManager.character_dict["Joe"] = Character(name="Steve", intro_text="It's Joe")
        CharacterManager.character_dict["Mama"] = Character(name="Steve", intro_text="And I'm Mama")
        self.enter_current_room()
        self.grid_manager.set_root_container(self)

    def interact_with_character(self, character):
        self.update_context_menu(character.get_character_command_dict())
        self.update_log(DialogueManager.story.get_story_log())
        #self.update_log(character.get_intro_text())

    def enter_current_room(self):
        self.enter_room(self.room_manager.room_map.current_room)

    def enter_room(self, room):
        self.update_log(room.get_room_desc())
        self.update_context_menu(room.get_room_command_dict())

    def update_log(self, new_text):
        self.scrollable_widget.update_text(new_text)

    def dialogue_pressed(self, story):
        self.update_log(story.get_story_log())
        self.update_context_menu(story.get_story_commands())

    def update_context_menu(self, command_dict):
        self.grid_manager.clear_buttons()
        top_row_iter = 0
        for key, command in command_dict.items():
            if isinstance(command, InteractCommand):
                if self.grid_manager.button_list[top_row_iter].has_command():
                    top_row_iter += 1
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
                else:
                    self.grid_manager.button_list[top_row_iter].set_command(command)
                    self.grid_manager.button_list[top_row_iter].set_display_text(key)
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
