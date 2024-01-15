import asyncio, logging, time
import covers
from collections.abc import Mapping


class DictCache:

    _dict_cache = {
        "message": "",
        "images": {
            "day": {
                "sizes": [
                    {"resolution": [], "size": 0, "url": ""}
                ],
                "author": "", "source": "",
                "featured": False
            },
            "night": {
                "sizes": [
                    {"resolution": [], "size": 0, "url": ""}
                ],
                "author": "", "source": "",
                "featured": False
            },
            "pic": ""
        },
        "streams": {
            "sample": {
                "name":        {"en": "", "ru": ""},
                "description": {"en": "", "ru": ""},
                "source":      {"mime": "", "bitrate": "", "url": ""},
                "listeners":   0,
            }
        },
        "track": {
            "title": "", "artist": "",
            "album": "", "year":   0,
            "cover": "", "lyrics": "",
            "featured": False
        },
        "playlist": {
            "queue": [
                {"title": "", "artist": "", "time": 0, "duration": 0}
            ],
            "history": [
                {"title": "", "artist": "", "time": 0}
            ]
        },
        "live": {},
        "ads": {}
    }

    async def on_update(self, update):
        logging.warn("Callback not implemented")

    async def _commit(self, changes):
        # TODO: make decorator
        self._dict_cache = _deep_update(self._dict_cache, changes)
        await self.on_update({"update": changes})

    def _add_history(self, track):
        track = {key: track[key] for key in ["title", "artist"]}
        track["time"] = int(time.time())
        history = self._dict_cache["playlist"]["history"]
        history.insert(0, track)
        if len(history) > 10:
            history.pop(len(history) - 1)
        return history

    async def _add_cover(self, filename):
        # TODO: move coversdir ("covers") to config
        filename, mime = await covers.write("/root/" + filename, "/root/covers") or (None, None)
        return {"cover": {"mime": mime, "url": "https://wave.lampovi.site/api/covers/" + filename}}

    async def set_message(self, message):
        await self._commit({"message": message})

    async def set_streams(self, streams):
        commit = {}
        for stream in streams:
            commit.update({
                stream["name"]: {
                    "title": {
                        "en": stream["title.en"],
                        "ru": stream["title.ru"]
                    },
                    "description": {
                        "en": stream["description.en"],
                        "ru": stream["description.ru"]
                    },
                    "source": {
                        "mime": stream["mime"],
                        "url": stream["mount"]
                    }
                }
            })
        await self._commit({"streams": commit})

    async def set_listeners(self, stream, listeners):
        await self._commit({"streams": {stream: {"listeners": listeners}}})

    async def set_track(self, track):
        history = self._add_history(track)
        # cover = await self._add_cover(track["filename"])
        track = {k: v for k, v in track.items() if k in ["title", "artist", "album", "year", "lyrics", "lyrics-rus", "lyrics-eng"]}
        track = self._fix_track_lyrics(track)
        # track.update(cover)
        await self._commit({"playlist": {"history": history}, "track": track})

    def _fix_track_lyrics(self, track):
        # TODO: make str.strip for each line
        for k in track.keys():
            if k.startswith("lyrics"):
                track[k] = track[k].replace("\r", "")
        return track

    def get_bootstrap(self):
        return {"bootstrap": self._dict_cache}

### Utils

# From https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth/63543967#63543967
def _deep_update(d1, d2):
    if all((isinstance(d, Mapping) for d in (d1, d2))):
        for k, v in d2.items():
            d1[k] = _deep_update(d1.get(k), v)
        return d1
    return d2