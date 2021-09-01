import kivy
kivy.require('2.0.0')
from kivy.app import App
from RoomManager import Room, RoomManager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class LeftPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(LeftPanelWidget, self).__init__(**kwargs)


class RightPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(RightPanelWidget, self).__init__(**kwargs)


class CenterPanelWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CenterPanelWidget, self).__init__(**kwargs)


class GameContainer(BoxLayout):
    room_manager = ObjectProperty()
    grid_manager_widget = ObjectProperty()
    scrollable_widget = ObjectProperty()

    def __init__(self, **kwargs):
        super(GameContainer, self).__init__(**kwargs)
        self.room_manager = RoomManager()
        if self.room_manager:
            print("created: " + str(self.room_manager))
            print("this container is " + str(self))
        home = Room("Home")
        self.room_manager.add_room(home)
        left_room = Room("Left Room")
        self.room_manager.add_room(left_room)
        right_room = Room("Right Room")
        self.room_manager.add_room(right_room)
        self.room_manager.add_connection(home, "Left", left_room, "Right")
        self.room_manager.add_connection(home, "Right", right_room, "Left")
        self.grid_manager_widget.set_room_manager_ref(self.room_manager)

    def assign_grid_manager_widget(self, widget):
        if self.grid_manager_widget:
            print("Error: tried to create extra grid manager widget")
        else:
            self.grid_manager_widget = widget

    def assign_scrollable_widget(self, widget):
        if self.scrollable_widget:
            print("Error: tried to create extra grid manager widget")
        else:
            self.scrollable_widget = widget

    def handle_button_presses(self, text):
        self.room_manager.travel(text)
        self.scrollable_widget.add_text(text)
