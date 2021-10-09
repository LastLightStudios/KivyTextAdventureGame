import kivy
kivy.require('2.0.0')
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, ObjectProperty,  StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class DynamicStatBar(BoxLayout):
    root_container = ObjectProperty()
    display_text = StringProperty("Stat")
    maximum_value = NumericProperty()
    current_value = NumericProperty()
    current_percent = NumericProperty()
    current_size = ListProperty([0, 0])
    display_value = StringProperty()
    background_color = ListProperty([0.1, 0.1, 0.1])
    foreground_color = ListProperty([0.8, 0.1, 0.1, 1.0])

    def __init__(self, **kwargs):
        super(DynamicStatBar, self).__init__(**kwargs)
        self.bind(size=self.update_bar_visual)
        self.set_max_value(100)
        self.set_current_value(50)

    # for some reason the size is getting called again after everything is made and messing everything up
    def update_bar_visual(self, *args):
        print(str(self.fill_bar.size))
        self.current_size = [self.current_percent * self.fill_bar.size[0], self.fill_bar.size[1]]
        print(str(self.current_size))
        self.display_value = str(self.current_value) + "/" + str(self.maximum_value)

    def set_max_value(self, value):
        self.maximum_value = value

    def set_current_value(self, value):
        self.current_value = value
        self.current_percent = (max(0, min(self.maximum_value, value))) / self.maximum_value
        self.update_bar_visual()
        print("Updated bar")


class CharacterStatBlockDisplay(BoxLayout):
    root_container = ObjectProperty()
    character_name = StringProperty()
    stat_dict = {}

    def __init__(self, **kwargs):
        super(CharacterStatBlockDisplay, self).__init__(**kwargs)
        health_bar = DynamicStatBar()
        self.stat_dict["Health_Bar"] = health_bar
        self.add_widget(health_bar)

    def set_root_container(self, root_container):
        self.root_container = root_container
        DynamicStatBar.root_container = self.root_container

    def init_health(self, max_hp):
        self.stat_dict["Health_Bar"].set_max_value(max_hp)
        self.stat_dict["Health_Bar"].set_current_value(max_hp)

    def update_health(self, current_hp, max_hp):
        print("Updating")
        self.stat_dict["Health_Bar"].set_max_value(max_hp)
        self.stat_dict["Health_Bar"].set_current_value(current_hp)
