import kivy

kivy.require('2.0.0')
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from ContextMenu import DynamicButton

"""

two part Boxlayout:
a button - Character(s) (number in list)

ScrollView
holds a Grid Layout 

"""


class KivyCharacterManager(BoxLayout):
    display_text = StringProperty("placeholder")

    def __init__(self, **kwargs):
        super(KivyCharacterManager, self).__init__(**kwargs)

    def change_display_text(self, new_text):
        self.display_text = new_text


class ListScrollManager(GridLayout):
    button_list = []

    def __init__(self, **kwargs):
        super(ListScrollManager, self).__init__(**kwargs)
        for i in range(0, 15):
            button = DynamicButton()
            self.button_list.insert(i, button)
            self.add_widget(button)
