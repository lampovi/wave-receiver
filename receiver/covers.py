import asyncio
import aiofiles
import os
import mimetypes
import time
import mutagen

async def _find(filepath):
    directory = os.path.dirname(filepath)
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path) and item.lower().startswith("cover."):
            mime = mimetypes.guess_type(path)
            extension = mimetypes.guess_extension(mime)
            data = await aiofiles.open(path).read()
            return data, extension, mime

async def get(filepath):
    loop = asyncio.get_running_loop()
    audio = await loop.run_in_executor(None, mutagen.File, filepath)
    audio = mutagen.File(filepath)
    if isinstance(audio, mutagen.mp3.MP3):
        apic = audio.tags.get("APIC:")
        if apic:
            extension = mimetypes.guess_extension(apic.mime, strict=False)
            return apic.data, extension, apic.mime
    return await _find(filepath)

async def write(filepath, coverdir):
    data, extension, mime = await get(filepath) or (None, None, None)
    if not (data and extension):
        return
    cover_filename = str(int(time.time())) + extension
    cover_path = os.path.join(coverdir, cover_filename)
    async with aiofiles.open(cover_path, "wb") as f:
        await f.write(data)
    return cover_filename, mime