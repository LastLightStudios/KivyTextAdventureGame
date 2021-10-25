import kivy

kivy.require('2.0.0')
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

""" View info """
from KivyPy.ContextMenu import DynamicButton

""" Model info """
import Game.GameState as GameState
from Game.Commands import InteractCommand

"""

two part Boxlayout:
a button - Character(s) (number in list)

ScrollView
holds a Grid Layout 

"""


class KivyCharacterManager(BoxLayout):
    list_scroll_manager = ObjectProperty()
    display_text = StringProperty("Characters: (0)")

    def __init__(self, **kwargs):
        super(KivyCharacterManager, self).__init__(**kwargs)
        GameState.register("Commands", self)

    def listener_event(self, info):
        if "Commands" in info:
            self.update_character_list(info["Commands"])


    def change_display_text(self, new_text):
        self.display_text = new_text

    def update_character_list(self, command_dict):
        self.list_scroll_manager.clear_widgets()
        count = 0
        for key, command in command_dict.items():
            if isinstance(command, InteractCommand):
                count += 1
                button = DynamicButton()
                button.set_display_text(key)
                button.set_command(command)
                self.list_scroll_manager.add_widget(button)
        self.change_display_text("Characters: (" + str(count) + ")")


class ListScrollManager(GridLayout):
    button_list = []

    def __init__(self, **kwargs):
        super(ListScrollManager, self).__init__(**kwargs)
