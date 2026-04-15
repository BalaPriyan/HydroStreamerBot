# This file is a part of FileStreamBot

import sys
import asyncio
import logging
import logging.handlers as handlers
from .vars import Var
from aiohttp import web
from WebStreamer.server import web_server

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
# Unmute aiohttp and aiohttp.web for production observability
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("aiohttp.web").setLevel(logging.WARNING)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    try:
        import winloop
        asyncio.set_event_loop_policy(winloop.EventLoopPolicy())
    except ImportError:
        pass

if __name__ == "__main__":
    app = web_server()
    web.run_app(app, host=Var.BIND_ADDRESS, port=Var.PORT)
