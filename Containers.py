import kivy
kivy.require('2.0.0')
from RoomManager import Room, RoomManager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from Commands import TravelCommand


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
        self.room_manager = RoomManager()
        self.room_manager.create_new_map()
        self.grid_manager.set_room_manager_ref(self.room_manager)
        self.grid_manager.set_commands(self)

    def move_rooms(self, direction):
        if self.room_manager.map.travel(direction):
            self.scrollable_widget.add_text(self.room_manager.map.get_current_room_desc())
            self.update_context_menu()

    def update_context_menu(self):
        self.grid_manager.clear_button_text()
        for key in self.room_manager.map.current_room.connected_rooms:
            self.grid_manager.button_list[self.convert_dir_to_button(key)].set_command(TravelCommand(self, key))
            self.grid_manager.button_list[self.convert_dir_to_button(key)].set_display_text(key)

    @staticmethod
    def convert_dir_to_button(direction):
        switcher = {
            "Forward": 1,
            "Left": 5,
            "Backward": 6,
            "Right": 7
        }
        return switcher.get(direction)
