import kivy

kivy.require('2.0.0')
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

""" View info """
from ContextMenu import DynamicButton
from StatDisplay import CharacterStatBlockDisplay

""" Model info """
from Game import GameState
from Game.Commands import InteractCommand

"""

two part Boxlayout:
a button - Character(s) (number in list)

ScrollView
holds a Grid Layout 

"""


class PartyStatBlockDisplayManager(BoxLayout):
    list_scroll_manager = ObjectProperty()
    display_text = StringProperty("Party: (0)")

    def __init__(self, **kwargs):
        super(PartyStatBlockDisplayManager, self).__init__(**kwargs)
        self.list_scroll_manager.change_content_size(3)

    def change_display_text(self, new_text):
        self.display_text = new_text

    """Expecting to receive a list of characters"""
    def update_character_list(self, char_list):
        self.list_scroll_manager.clear_widgets()
        count = 0
        for character in char_list:
            new_char_stat = CharacterStatBlockDisplay(size_hint_y=0.3)
            new_char_stat.change_character_name(character.name)
            new_char_stat.update_health(character.health, character.max_health)
            self.list_scroll_manager.add_widget(new_char_stat)
        self.change_display_text("Party: (" + str(count) + ")")