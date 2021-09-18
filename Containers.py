import kivy
kivy.require('2.0.0')
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

import RoomManager
from Commands import InteractCommand, TravelCommand


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
        self.enter_room(self.room_manager.room_map.current_room)
        self.grid_manager.set_root_container(self)

    def enter_room(self, room):
        self.update_log(room.get_room_desc())
        self.update_context_menu(room.get_room_command_dict())

    def update_log(self, new_text):
        self.scrollable_widget.add_text(new_text)

    def move_rooms(self, direction):
        if self.room_manager.room_map.travel(direction):
            self.scrollable_widget.add_text(self.room_manager.room_map.get_current_room_desc())
            self.update_context_menu()

    def update_context_menu(self, command_dict):
        self.grid_manager.clear_buttons()
        char_iter = 0
        for key, command in command_dict.items():
            if isinstance(command, InteractCommand):
                if self.grid_manager.button_list[char_iter].has_command():
                    char_iter += 1
                    self.grid_manager.button_list[char_iter].set_command(command)
                    self.grid_manager.button_list[char_iter].set_display_text(key)
                else:
                    self.grid_manager.button_list[char_iter].set_command(command)
                    self.grid_manager.button_list[char_iter].set_display_text(key)
            elif isinstance(command, TravelCommand):
                self.grid_manager.button_list[self.convert_dir_to_button(key)].set_command(command)
                self.grid_manager.button_list[self.convert_dir_to_button(key)].set_display_text(key)
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
