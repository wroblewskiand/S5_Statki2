from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import plane

class Statki(GridLayout):

    def __init__(self, **kwargs):
        super(Statki, self).__init__(**kwargs)
        self.ids['przeciwnik'].disabled = True

    def startButtonClick(self):
        self.ids['gracz'].disabled = True
        self.ids['przeciwnik'].disabled = False
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")
        
class StatkiApp(App):
    
    def build(self):
        return Statki()

if __name__ == '__main__':
    Config.read('config.ini')
    StatkiApp().run()