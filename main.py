import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from Containers import GameContainer
# importing Widgets that PyCharm shows as unused. They are used in the kv file
from ContextMenu import GridManager


class ScrollableWidget(ScrollView):
    text = StringProperty('Welcome \n')

    def init_complete(self):
        for child in self.children:
            pass

    def add_text(self, text):
        self.text += text + '\n'


class TestApp(App):
    def build(self):
        return GameContainer()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TestApp().run()
