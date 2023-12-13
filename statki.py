from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import plane
from gamebutton import GameButton

class Statki(GridLayout):

    isGameStarted = False

    def __init__(self, **kwargs):
        super(Statki, self).__init__(**kwargs)
        self.ids['przeciwnik'].disabled = True

        for c1 in self.children:
            for c2 in c1.children:
                for c3 in c2.children:
                    for c4 in c3.children:
                        if isinstance(c4, GameButton):
                            c4.sendMessage = self.sendMessage

    def startButtonClick(self):
        self.ids['gracz'].disabled = True
        self.ids['przeciwnik'].disabled = False
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")
        self.isGameStarted = True

    def onMessage(self, message):
        x = str(message['x'])
        y = str(message['y'])
        if self.isShip(x, y):
            self.ids['przeciwnik'].ids[y].ids[x].hit()
        else: self.ids['przeciwnik'].ids[y].ids[x].miss()

    def sendMessage(self, message):
        if not self.isGameStarted:
            return
        
        print(message)
        self.onMessage(message)

    def isShip(self, x: str, y: str):
        # print(f'y: {y}, x: {y}')
        return self.ids['gracz'].ids[y].ids[x].isShip
        
class StatkiApp(App):
    
    def build(self):
        return Statki()

if __name__ == '__main__':
    Config.read('config.ini')
    StatkiApp().run()