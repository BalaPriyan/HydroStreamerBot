import asyncio
from aiohttp import web
from WebStreamer.vars import Var
from WebStreamer.bot import StreamBot
from WebStreamer.utils import ping_server
from WebStreamer.bot.clients import initialize_clients
from WebStreamer.utils.database import db

from .stream_routes import routes
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, rate=60, per=60):
        self.rate = rate
        self.per = per
        self.allowance = defaultdict(lambda: self.rate)
        self.last_check = defaultdict(time.monotonic)

    async def middleware(self, app, handler):
        async def middleware_handler(request):
            ip = request.headers.get("X-FORWARDED-FOR", request.remote)
            if request.path.startswith("/stats"):
                return await handler(request)

            current = time.monotonic()
            time_passed = current - self.last_check[ip]
            self.last_check[ip] = current
            self.allowance[ip] += time_passed * (self.rate / self.per)
            if self.allowance[ip] > self.rate:
                self.allowance[ip] = self.rate
            if self.allowance[ip] < 1.0:
                raise web.HTTPTooManyRequests(text="429: Too Many Requests")
            else:
                self.allowance[ip] -= 1.0
                return await handler(request)
        return middleware_handler

limiter = RateLimiter(rate=120, per=60) # 120 reqs per minute

async def start_services(app):
    print("-------------------- Initializing Telegram Bot --------------------")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.id = bot_info.id
    StreamBot.username = bot_info.username
    StreamBot.fname = bot_info.first_name
    print("------------------------------ DONE ------------------------------")
    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print("---------------------- Initializing Database ----------------------")
    await db.setup()
    print("------------------------------ DONE ------------------------------")
    if Var.KEEP_ALIVE:
        print("------------------ Starting Keep Alive Service ------------------")
        asyncio.create_task(ping_server())

async def stop_services(app):
    print("---------------------- Stopping Services ----------------------")
    await StreamBot.stop()

def web_server():
    web_app = web.Application(
        client_max_size=30000000,
        middlewares=[limiter.middleware]
    )
    web_app.on_startup.append(start_services)
    web_app.on_cleanup.append(stop_services)
    web_app.add_routes(routes)
    return web_app
