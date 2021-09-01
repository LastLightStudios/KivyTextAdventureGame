import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class LeftPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(LeftPanelWidget, self).__init__(**kwargs)


class RightPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(RightPanelWidget, self).__init__(**kwargs)


class CenterPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(CenterPanelWidget, self).__init__(**kwargs)


class ActionMenuWidget(Widget):
    def __init__(self, **kwargs):
        super(ActionMenuWidget, self).__init__(**kwargs)


class DynamicButton(Widget):
    display_text = NumericProperty("0")

    def __init__(self, **kwargs):
        super(DynamicButton, self).__init__(**kwargs)

    def on_press(self):
        self.increment()

    def increment(self):
        self.display_text += 1


class GridManager:
    ButtonList = []
    parent_widget = None

    def create_button_grid(self, parent_widget):
        for i in range(0, 15):
            parent_widget.add_widget(Button(text="Button {0}".format(i)))


class SpecialButton(Button):
    def __init__(self, **kwargs):
        super(SpecialButton, self).__init__(**kwargs)


class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)


class TestApp(App):
    def build(self):
        return ContainerBox()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TestApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
