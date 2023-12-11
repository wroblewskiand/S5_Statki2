from kivy.uix.button import Button
from kivy.properties import BooleanProperty, DictProperty

class GameButton(Button):
    coordinate = DictProperty({"x": 0, "y": 0})
    isShip = BooleanProperty(False)

    def on_release(self):
        super(GameButton, self).on_release()
        self.isShip = not self.isShip
        self.updateColor()
        print(self.coordinate)
        

    def updateColor(self):
        if self.isShip:
            self.background_color = (0, 0, 0.9)
        else:
            self.background_color = (0.99, 0.99, 0.99)