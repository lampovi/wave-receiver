import pytest
from linker import cache

track_sample = {
    "album": "Товарищ память",
    "date": "2016",
    "track": "1",
    "encoded_by": "LAME in FL Studio 11",
    "kind": "{audio=2;video=0;midi=0}",
    "year": "2016",
    "artist": "Перемотка",
    "decoder": "FFMPEG",
    "title": "Взгляд",
    "bpm": "130",
    "filename": "music/regular/Товарищ память (2016)/Перемотка – Товарищ память (2016) – 01. Взгляд.mp3",
    "temporary": "false",
    "source": "regular",
    "tracknumber": "1",
    "initial_uri": "music/regular/Товарищ память (2016)/Перемотка – Товарищ память (2016) – 01. Взгляд.mp3",
    "playlist_length": "4",
    "status": "playing",
    "encodedby": "LAME in FL Studio 11",
    "tbpm": "130",
    "on_air": "2020/05/07 22:05:57",
    "rid": "1",
    "playlist_position": "0"
}

streams_sample = [
    {
        "name": "default",
        "title.en": "Default stream",
        "title.ru": "Стандартный поток",
        "description.en": "Main stream of Lampovi Wave",
        "description.ru": "Основной поток Ламповой Волны",
        "mount": "default/stream.ogg",
        "mime": "audio/ogg",
        "listeners": "0"
    },
    {
        "name": "music_only",
        "title.en": "Music only",
        "title.ru": "Только музыка",
        "description.en": "No live broadcasts, jingles, etc.",
        "description.ru": "Без эфиров и вставок",
        "mount": "music_only/stream.ogg",
        "mime": "audio/ogg",
        "listeners": "0"
    },
    {
        "name": "low",
        "title.en": "Low quality",
        "title.ru": "Сжатый поток",
        "description.en": "For listeners with unstable connection",
        "description.ru": "Для слушателей со слабым соединением",
        "mount": "low/stream.ogg",
        "mime": "audio/ogg",
        "listeners": "0"
    },
    {
        "name": "white_noise",
        "title.en": "White noise",
        "title.ru": "Белый шум",
        "description.en": "It's a music too",
        "description.ru": "Это тоже музыка",
        "mount": "white_noise/stream.wav",
        "mime": "audio/wav",
        "listeners": "0"
    }
]

def test_set_streams():
    pass