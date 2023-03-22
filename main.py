import kivy

from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

kivy.require('2.1.0')


class FibTreeVisSim(Widget):
    pass

class FibTreeVisApp(App):

    def build(self):
        Window.size = (1280,720)
        sim = FibTreeVisSim()
        return sim


if __name__ == '__main__':
    FibTreeVisApp().run()
