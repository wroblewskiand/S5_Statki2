from kivy import Config
from statki import StatkiApp

if __name__ == '__main__':
    Config.read('config.ini')
    StatkiApp().run()