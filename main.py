import kivy

from kivy.app import App
from kivy.uix.widget import Widget
kivy.require('2.1.0')



class PongGame(Widget):
    pass

class PongApp(App):

    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()