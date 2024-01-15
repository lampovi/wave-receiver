import json
import functools
from aiohttp import web
from aiohttp import WSMsgType

class Frontend():
    def __init__(self, cache):
        self.app = web.Application()
        self.app.add_routes([
            web.get("/api/ws", self.ws_serve),
            web.get("/api/ping", self.ping),
            web.static("/api/cover", "/root/covers")
        ])
        self.cache = cache
        self.app["websockets"] = []

    async def broadcast(self, data):
        for client in self.app["websockets"]:
            await client.send_json(data, dumps=self.dumps)


    async def ws_serve(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.app["websockets"].append(ws)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    data = msg.json()
                except json.decoder.JSONDecodeError:
                    await ws.send_json({"error": "Can't decode JSON"})
                    continue
                if data["request"] == "bootstrap":
                    await ws.send_json(self.cache.get_bootstrap(), dumps=self.dumps)
            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
        await ws.close()
        self.app["websockets"].remove(ws)
        return ws

    async def ping(self, request):
        return web.Response(text="ping")

    dumps = functools.partial(json.dumps, ensure_ascii=False)

class Backend():

    def __init__(self, cache):
        self.app = web.Application()
        self.app.add_routes([
            web.post("/track", self.post_track),
            web.post("/streams", self.post_streams),
            web.post("/listeners", self.post_listeners)
        ])
        self.cache = cache

    async def post_track(self, request):
        data = await request.json()
        await self.cache.set_track(data)
        return web.Response(text="ok.")

    async def post_streams(self, request):
        data = await request.json()
        await self.cache.set_streams(data)
        return web.Response(text="ok.")

    async def post_listeners(self, request):
        stream = request.query["stream"]
        data = await request.json()
        await self.cache.set_listeners(stream, data)
        return web.Response(text="ok.")
