from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class Statki(GridLayout):

    def __init__(self, **kwargs):
        super(Statki, self).__init__(**kwargs)


class StatkiApp(App):
    
    def build(self):
        return Statki()

if __name__ == '__main__':
    Config.read('config.ini')
    StatkiApp().run()