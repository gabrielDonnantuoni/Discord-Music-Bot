import gtts
from ytdl.config import ffmpeg_options
import discord

class TTSSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, volume=0.5):
        super().__init__(source, volume)

    @classmethod
    def from_str(cls, string):
        tts = gtts.gTTS(string, lang='pt-br')
        tts.save('tts.mp3')
        return cls(discord.FFmpegPCMAudio('tts.mp3', **ffmpeg_options))
