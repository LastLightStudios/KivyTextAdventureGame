import kivy
kivy.require('2.0.0')
from RoomManager import Room, RoomManager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


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

    def handle_button_presses(self, text):
        scroll_text = self.room_manager.travel(text)
        self.scrollable_widget.add_text(scroll_text)
