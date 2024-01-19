import asyncio
import plane

from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from client import Client
from gamebutton import GameButton
from message import Message


class Statki(GridLayout):

    def __init__(self, **kwargs):
        super(Statki, self).__init__(**kwargs)
        self.isGameStarted = False
        self.client = Client(self.onMessage)
        self.ids['przeciwnik'].disabled = True
        self.lastX = 0
        self.lastY = 0

        for c1 in self.children:
            for c2 in c1.children:
                for c3 in c2.children:
                    for c4 in c3.children:
                        if isinstance(c4, GameButton):
                            c4.sendMessage = self.sendMessage
                            c4.saveLastHitPosition = self.saveLastHitPosition

    def saveLastHitPosition(self, x, y):
        self.lastX = x
        self.lastY = y

    def startButtonClick(self):
        self.ids['gracz'].disabled = True
        self.ids['przeciwnik'].disabled = False
        self.ids['startGameButton'].disabled = True
        self.ids['gameId'].disabled = True
        print("Click")
        self.isGameStarted = True
        self.sendMessage(Message.PlayerConnectedMessage())

    def onMessage(self, message: Message.BaseMessage):

        if message.type == Message.BaseMessage.ATTACK:
            x = message.x
            y = message.y
            self.ids['gracz'].ids[str(y)].ids[str(x)].setWasHit()

            if self.isShip(x, y) and self.isSunken(x, y, {}):
                self.sank(x, y, {}, 'gracz')
                self.sendMessage(Message.SankMessage())
            elif self.isShip(x, y):
                # self.ids['przeciwnik'].ids[str(y)].ids[str(x)].hit()
                self.sendMessage(Message.HitMessage())
            else: 
                # self.ids['przeciwnik'].ids[str(y)].ids[str(x)].miss()
                self.sendMessage(Message.MissMessage())
        elif message.type == Message.BaseMessage.SANK:
            self.sank(self.lastX, self.lastY, {}, 'przeciwnik')
        elif message.type == Message.BaseMessage.HIT:
            self.ids['przeciwnik'].ids[str(self.lastY)].ids[str(self.lastX)].hit()
        elif message.type == Message.BaseMessage.MISS:
            self.ids['przeciwnik'].ids[str(self.lastY)].ids[str(self.lastX)].miss()

    def sendMessage(self, message):
        if not self.isGameStarted:
            return
        self.client.sendMessage(message)
        # print(message)
        # self.onMessage(message)

    def isShip(self, x: int, y: int):
        # print(f'y: {y}, x: {y}')
        return self.ids['gracz'].ids[str(y)].ids[str(x)].isShip
    
    def wasHit(self, x: int, y: int):
        return self.ids['gracz'].ids[str(y)].ids[str(x)].wasHit
    
    def isSunken(self, x, y, visited):
        if not self.isShip(x, y):
            return False
        
        if (x, y) not in visited:
            if self.wasHit(x, y):
                visited[(x, y)] = True

                for i in range(y - 1, y + 2):
                    if i == 0 or i == 11:
                        continue
                    for j in range(x - 1, x + 2):
                        if j == 0 or j == 11 or (i == y and j == x):
                            continue
                        if  self.isShip(j, i) and not self.isSunken(j, i, visited):
                            return False

            else:
                return False

        return True

    def sank(self, x, y, visited, tag = 'przeciwnik'):
        if (x, y) not in visited:
            visited[(x, y)] = True
            for i in range(y-1, y+2):
                if i == 0 or i == 11:
                    continue
                for j in range(x-1, x+2):
                    if j == 0 or j == 11:
                        continue
                    self.ids[tag].ids[str(y)].ids[str(x)].setWasHit()
                    if self.ids[tag].ids[str(y)].ids[str(x)].isShip:
                        self.sank(j, i, visited, tag)


class StatkiApp(App):
    
    async def async_run(self, async_lib=None):
        self.load_config()
        self.load_kv(filename=self.kv_file)
        self.root = Statki()
        
        await asyncio.gather(super(StatkiApp, self).async_run(async_lib=async_lib), self.root.client.run())

    def stop(self):
        self.root.client.stop()
        super(StatkiApp, self).stop()   