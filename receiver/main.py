import logging
import asyncio
import aiohttp

import cache
import sides

cache = cache.DictCache()
frontend = sides.Frontend(cache)
backend = sides.Backend(cache)
cache.on_update = frontend.broadcast

logging.basicConfig(
    format="{levelname} | {message}",
    style="{", level=logging.INFO
)

# Warning! Stack overflow code!

runners = []

async def start_site(app, address, port):
    runner = aiohttp.web.AppRunner(app)
    runners.append(runner)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, address, port)
    await site.start()


loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.create_task(start_site(frontend.app, "0.0.0.0", 8001))
loop.create_task(start_site(backend.app, "0.0.0.0", 8002))

try:
    loop.run_forever()
except:
    pass
finally:
    for runner in runners:
        loop.run_until_complete(runner.cleanup())
