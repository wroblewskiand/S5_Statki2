import time
import asyncio
import websockets

from backend.game import Game

# from backend.game import Game

class Server:

    clients = {}
    games = {}              # Id, obiekt gry
    websocketToGame = {}    # websocket, Id gry

    gameKeys = ['A', 'B', 'C']

    def __init__(self):
        self.clients = {}

    async def echo(self, websocket, path):
        try:
            async for message in websocket:

                if websocket is self.websocketToGame:
                    game = self.websocketToGame[websocket]
                    if len(game.players) == 2:
                        await game.handle(websocket, message)  

                else:
                    self.websocketToGame[websocket] =  self.gameKeys[round(len(self.websocketToGame) /2)]

                    if self.websocketToGame[websocket] in self.games:
                        self.games[self.websocketToGame[websocket]].add_player(websocket)

                    else:
                        self.games[self.websocketToGame[websocket]] = Game()
                        self.games[self.websocketToGame[websocket]].add_player(websocket)

                    # if not self.websocketToGame[websocket] in self.games:
                    #     self.games[self.websocketToGame[websocket]] = Game()

                    # if len(self.websocketToGame) % 2:
                    #     self.games[self.websocketToGame[websocket]] = Game()

                # print(time.strftime("%X"), "handling message: ", message)
                # await asyncio.sleep(1)
                # await websocket.send(message)
                # print("Message handle finished", message)


                # if websocket not in self.clients:
                #     self.clients[websocket] = True

                # for key in self.clients:
                #     if key == websocket:
                #         continue
                #     await key.send(message)
                
                # await websocket.send(message)

        except RuntimeError:
            print("Error")


s = Server()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(s.echo, 'localhost', 8765)
)

asyncio.get_event_loop().run_forever()