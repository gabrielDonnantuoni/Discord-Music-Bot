# import youtube_dl
import yt_dlp
import discord
import asyncio
from ytdl.config import ytdl_format_options, ffmpeg_options, yt_url_pattern
from googleapiclient.discovery import build
from env import GOOGLE_API_TOKEN

yt_dlp.utils.bug_reports_message = lambda: ''
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)
yt_api = build('youtube', 'v3', developerKey=GOOGLE_API_TOKEN)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(
            discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    def rebuild(self, volume=0.5):
        super().__init__(discord.FFmpegPCMAudio(self.url, **ffmpeg_options), volume)
    
    @classmethod
    async def extract_info(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        print(data['url'])

    @classmethod
    async def from_query(cls, query, *, index = 0, loop=None, stream=True):
        response = yt_api.search().list(
            part='id',
            maxResults=3,
            q=query
        ).execute()

        id_obj = response['items'][index]['id']
        kind = id_obj['kind']

        url = None
        try:
            url_pattern = yt_url_pattern[kind]['pattern']
            id = id_obj[yt_url_pattern[kind]['id']]
            url = url_pattern + id
        except KeyError:
            pass

        if not url:
            return None
        return await cls.from_url(url)

def get_audio_source(db_song):
    return YTDLSource(
        discord.FFmpegPCMAudio(db_song['url'], **ffmpeg_options), data=db_song)