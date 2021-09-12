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
        home.set_desc("This is the starting room.")
        self.room_manager.add_room(home)
        left_room = Room("Left Room")
        left_room.set_desc("Welcome to the Left Room.")
        self.room_manager.add_room(left_room)
        right_room = Room("Right Room")
        right_room.set_desc("Welcome to the dining room.")
        self.room_manager.add_room(right_room)
        porch = Room("Porch")
        porch.set_desc("This is the porch. There is a new nice view of the street.")
        self.room_manager.add_room(porch)
        living_room = Room("Living Room")
        living_room.set_desc("This is living room. You can see a nice couch. To the right you can see the kitchen.")
        kitchen = Room("Kitchen")
        kitchen.set_desc("This is the kitchen. There is a dirty pot on the stove and two more in the sink.")
        self.room_manager.add_connection(home, "Left", left_room, "Right")
        self.room_manager.add_connection(home, "Right", right_room, "Left")
        self.room_manager.add_connection(home, "Forward", living_room, "Backwards")
        self.room_manager.add_connection(right_room, "Forward", kitchen, "Backwards")
        self.room_manager.add_connection(living_room, "Right", kitchen, "Left")
        self.grid_manager_widget.set_room_manager_ref(self.room_manager)
        for child in self.children:
            child.init_complete()

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
        scroll_text = self.room_manager.travel(text)
        self.scrollable_widget.add_text(scroll_text)
