import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class LeftPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(LeftPanelWidget, self).__init__(**kwargs)


class RightPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(RightPanelWidget, self).__init__(**kwargs)


class CenterPanelWidget(Widget):
    def __init__(self, **kwargs):
        super(CenterPanelWidget, self).__init__(**kwargs)


class GameContainer(BoxLayout):
    def __init__(self, **kwargs):
        super(GameContainer, self).__init__(**kwargs)
