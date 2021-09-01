import kivy
from RoomManager import RoomManager, Room
kivy.require('2.0.0')
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from Containers import GameContainer, LeftPanelWidget, CenterPanelWidget, RightPanelWidget


class GridButtons(GridLayout):
    button_list = []
    a = StringProperty("a")

    def __init__(self, **kwargs):
        super(GridButtons, self).__init__(**kwargs)
        for i in range(0, 15):
            button = DynamicButton(self.a)
            self.button_list.insert(i, button)
            self.add_widget(button)
            self.a += "a"
        self.temp_set_directions()

    def temp_set_directions(self):
        self.button_list[1].set_display_text("Forward")
        self.button_list[5].set_display_text("Left")
        self.button_list[6].set_display_text("Backwards")
        self.button_list[7].set_display_text("Right")

    def button_pressed(self, text):
        self.parent.handle_button_presses(text)


class DynamicButton(Widget):
    display_text = StringProperty("0")

    def __init__(self, text, **kwargs):
        super(DynamicButton, self).__init__(**kwargs)
        self.display_text = text

    def on_press(self):
        self.parent.parent.parent.parent.handle_button_presses(self.display_text)

    def set_display_text(self, text):
        self.display_text = text


class GridManagerWidget(Widget):
    room_manager_ref = ObjectProperty()

    def __init__(self, **kwargs):
        super(GridManagerWidget, self).__init__(**kwargs)

    def on_parent(self, this, parent):
        self.parent.parent.assign_grid_manager_widget(self)

    def handle_button_presses(self, text):
        self.room_manager_ref.travel(text)

    def set_room_manager_ref(self, ref):
        self.room_manager_ref = ref
        print("assigned: " + str(self.room_manager_ref))


class ScrollableWidget(ScrollView):
    text = StringProperty('Test Test Test \n Test Test Test Test Test')

    def on_parent(self, this, parent):
        self.parent.parent.assign_scrollable_widget(self)

    def add_text(self, text):
        self.text += text + '\n'


class TestApp(App):
    def build(self):
        return GameContainer()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TestApp().run()
