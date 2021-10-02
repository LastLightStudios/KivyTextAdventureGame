import kivy
kivy.require('2.0.0')
from kivy.graphics import *
from kivy.properties import ListProperty, NumericProperty, ObjectProperty,  StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class DynamicStatBar(FloatLayout):
    root_container = ObjectProperty()
    fill_bar = ObjectProperty()
    maximum_value = NumericProperty()
    current_value = NumericProperty()
    current_percent = NumericProperty()
    current_size = NumericProperty()
    display_text = StringProperty()
    background_color = ListProperty([0.1, 0.1, 0.1])
    foreground_color = ListProperty([0.8, 0.1, 0.1, 1.0])

    def __init__(self, **kwargs):
        super(DynamicStatBar, self).__init__(**kwargs)
        self.set_max_value(100)
        self.set_current_value(50)
#        fill = Label(
#            text='test',
#            size_hint=(self.current_percent, 1.0),
#            pos_hint={'x': 0.5, 'y': 1.0})
#        with fill.canvas:
#            Color(self.foreground_color)
#            Rectangle(pos=fill.pos, size=fill.size)
#        self.add_widget(fill)

    def update_bar_visual(self):
        with self.fill_bar.canvas:
            Color(self.foreground_color)
            Rectangle(pos=self.pos, size=(self.size[0], self.size[1]*self.current_percent))

    def set_max_value(self, value):
        self.maximum_value = value

    def set_current_value(self, value):
        self.current_value = value
        self.current_percent = self.maximum_value / (max(0, min(self.maximum_value, value)))


class CharacterStatBlockDisplay(BoxLayout):
    root_container = ObjectProperty()

    def __init__(self, **kwargs):
        super(CharacterStatBlockDisplay, self).__init__(**kwargs)

    def set_root_container(self, root_container):
        self.root_container = root_container
        DynamicStatBar.root_container = self.root_container
