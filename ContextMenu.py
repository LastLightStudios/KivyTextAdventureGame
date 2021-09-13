import kivy
kivy.require('2.0.0')
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from Commands import TravelCommand


class DynamicButton(Widget):
    display_text = StringProperty("")

    def __init__(self, **kwargs):
        super(DynamicButton, self).__init__(**kwargs)
        self._command = None

    def on_press(self):
        if self._command:
            self._command.execute()

    def set_command(self, command):
        self._command = command

    def set_display_text(self, text):
        self.display_text = text


class GridManager(GridLayout):
    button_list = []
    room_manager_ref = ObjectProperty()

    def __init__(self, **kwargs):
        super(GridManager, self).__init__(**kwargs)
        self.root_container = ObjectProperty()
        for i in range(0, 15):
            button = DynamicButton()
            self.button_list.insert(i, button)
            self.add_widget(button)
        self.temp_set_directions()

    def set_commands(self, client):
        self.root_container = self.parent.parent.parent
        self.button_list[1].set_command(TravelCommand(client, "Forward"))
        self.button_list[5].set_command(TravelCommand(client, "Left"))
        self.button_list[6].set_command(TravelCommand(client, "Backward"))
        self.button_list[7].set_command(TravelCommand(client, "Right"))

    # the command_dict will be array_position:Command
    # TODO determine if this is a better way?
    def set_dynamic_commands(self, command_dict):
        pass

    def clear_button_text(self):
        for button in self.button_list:
            button.set_display_text("")

    def temp_set_directions(self):
        self.button_list[1].set_display_text("Forward")
        self.button_list[5].set_display_text("Left")
        self.button_list[6].set_display_text("Backwards")
        self.button_list[7].set_display_text("Right")


