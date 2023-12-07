from kivy.uix.button import Button
from kivy.properties import BooleanProperty

class GameButton(Button):
    isShip = BooleanProperty(False)

    def on_release(self):
        super(GameButton, self).on_release()
        self.isShip = not self.isShip
        self.updateColor()

    def updateColor(self):
        if self.isShip:
            self.background_color = (0, 0, 0.9)
        else:
            self.background_color = (0.99, 0.99, 0.99)