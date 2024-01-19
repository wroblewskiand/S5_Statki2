import asyncio

from kivy import Config
from statki import StatkiApp


if __name__ == '__main__':
    Config.read('config.ini')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        StatkiApp().async_run(async_lib='asyncio')
    )