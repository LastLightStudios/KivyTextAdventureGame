import kivy
kivy.require('2.0.0')
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget


class DynamicButton(Widget):
    root_container = ObjectProperty()
    display_text = StringProperty("")

    def __init__(self, **kwargs):
        super(DynamicButton, self).__init__(**kwargs)
        self.command = None

    def on_press(self):
        if self.command:
            self.command.execute(self.root_container)

    def set_command(self, command) -> None:
        self.command = command

    def has_command(self) -> bool:
        if self.command is not None:
            return True

    def set_display_text(self, text):
        self.display_text = text


class GridManager(GridLayout):
    button_list = []

    def __init__(self, **kwargs):
        super(GridManager, self).__init__(**kwargs)
        self.root_container = ObjectProperty()
        for i in range(0, 15):
            button = DynamicButton()
            self.button_list.insert(i, button)
            self.add_widget(button)

    def set_button_command_and_text(self, button_number, text, command):
        self.button_list[button_number].set_display_text(text)
        self.button_list[button_number].set_command(command)

    def set_root_container(self, root_container):
        self.root_container = root_container
        DynamicButton.root_container = self.root_container # I think this is changing the class property and thats why it works?

    def clear_buttons(self):
        for button in self.button_list:
            button.set_display_text("")
            button.set_command(None)

    def clear_button_text(self):
        for button in self.button_list:
            button.set_display_text("")
