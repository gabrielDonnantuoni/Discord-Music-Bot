import discord
from discord.ext import commands
from ytdl.YTDLSource import YTDLSource
from ytdl.TTS import TTSSource
from bot.Queue import Queue
import database.main as db 


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = None
        self.guild_id = None

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        '''Joins a voice channel'''

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def diz(self, ctx, *, query):
        source = TTSSource.from_str(query)
        await self.play(ctx, source)

    @commands.command()
    async def toca(self, ctx, *, query):
        '''Streams from a url (same as yt, but doesn't predownload)'''
        try_local = True
        await ctx.trigger_typing()

        if query.startswith('-'):
            options, query = query.split(' ', 1)
            if 'n' in options: # only new music
                try_local = False

        if query.startswith('https://'):
            source = await YTDLSource.from_url(query, loop=self.bot.loop)
        else:
            if try_local:
                source = self.queue.with_local_song(query)
                if not source:
                    source = await YTDLSource.from_query(query, loop=self.bot.loop)
            else:
                source = await YTDLSource.from_query(query, loop=self.bot.loop)
        
        await self.play(ctx, source)
    
    @commands.command()
    async def add(self, ctx, *, query):
        should_play = False
        if query.endswith(' e toca'):
            query = query.split(' e toca', 1)[0]
            should_play = True

        await ctx.trigger_typing()
        if should_play:
            await self.ensure_voice(ctx)

        if query.startswith('https://'):
            source = await YTDLSource.from_url(query, loop=self.bot.loop)
        else:
            source = await YTDLSource.from_query(query, loop=self.bot.loop)
        
        song = { 'title': source.title, 'url': source.url }

        if should_play:
            self.queue.add([song], should_update_index=True)
            await self.play(ctx, source)
        else:
            self.queue.add([song])
            await ctx.send(f'{source.title} adicionado a fila')

    @commands.command(aliases=['prox'])
    async def proxima(self, ctx, *, args=''):
        await self.skip(ctx)

    @commands.command(aliases=['ant'])
    async def anterior(self, ctx, *, args=''):
        await self.skip(ctx, foward=False)

    async def play(self, ctx, source):
        if ctx.voice_client.is_playing():
            ctx.voice_client.source = source
        else:
            if hasattr(source, 'title'):
                ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))
                await ctx.send(f'Tocando {source.title}')
            else:
                ctx.voice_client.play(source)

    async def skip(self, ctx, foward=True):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                source = self.queue.next() if foward else self.queue.prev()
                ctx.voice_client.source = source
            else:
                await ctx.send('Num ta nem tocando nada!')
        else:
            await ctx.send('Entra num canal pelo menos.')

    @commands.command()
    async def lista(self, ctx, *, args=''):
        await ctx.trigger_typing()
        lst = ''
        for idx, song in enumerate(self.queue.db_queue['song_list']):
            title = song['title']
            lst += f'{idx + 1} - {title}\n'
        
        if lst:
            await ctx.send(lst)
        else:
            await ctx.send('Lista ta vazia??a.')

    @commands.command()
    async def apaga(self, ctx, *, query=''):
        await ctx.trigger_typing()
        self.queue.remove(query)
        await ctx.send('Foi tudo que c?? pediu.')


    def play_next(self, ctx):
        if ctx.voice_client:
            source = self.queue.next()
            if source:
                ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))


    @commands.command()
    async def volume(self, ctx, volume: int):
        '''Changes the player's volume'''

        await ctx.trigger_typing()
        if ctx.voice_client is None:
            return await ctx.send('Mulher, tu nem ta conectada em um canal.')

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f'Volume alterado para [ {volume}% ]')

    @commands.command()
    async def vaza(self, ctx):
        '''Stops and disconnects the bot from voice'''
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send('J?? vazei fofx...')

    @commands.command()
    async def perai(self, ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
            elif ctx.voice_client.is_paused():
                await ctx.send('Mash, t?? fazendo nada...')
            else:
                await ctx.send('Oh beb??, pensa antes de escrever.')
        else:
            await ctx.send('Xuxu, nem conectado eu t??.')

    @commands.command()
    async def continua(self, ctx):
        if ctx.voice_client:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            elif ctx.voice_client.is_playing():
                await ctx.send('Ja ta tocando my love.')
            else:
                await ctx.send('Jovi, ninguem t?? entendendo o que c?? quer.')
        else:
            await ctx.send('Xuxu, nem conectado eu t??.')

    @commands.command()
    async def config(self, ctx, *, args=''):
        if args.startswith('keep_played'):
            if 'true' in args:
                self.queue.should_keep_played(True)
                await ctx.send('Config: keep_played = True')
            else:
                self.queue.should_keep_played(False)
                await ctx.send('Config: keep_played = True')
        else:
            await ctx.send('Sei que config ?? essa ai n??o.')


    @diz.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            # print('entrou')
            if ctx.author.voice:
                # print('passou aqui tbm')
                await ctx.author.voice.channel.connect()
            else:
                # print('ai ?? loucura')
                await ctx.trigger_typing()
                await ctx.send('Ohh... Tu nem t?? em um canal, man??.')
                raise commands.CommandError(
                    'Author not connected to a voice channel.')
        # elif ctx.voice_client.is_playing():
        #     ctx.voice_client.stop()
        #     print('era pra ter parado')

    @lista.before_invoke
    @proxima.before_invoke
    @anterior.before_invoke
    @add.before_invoke
    async def ensure_queue(self, ctx):
        guild_id = db.verify_guild_db(ctx)
        if not self.guild_id or self.guild_id != guild_id:
            self.guild_id = guild_id
            self.queue = Queue(guild_id)

    @toca.before_invoke
    async def ensure_voice_and_queue(self, ctx):
        await self.ensure_voice(ctx)
        await self.ensure_queue(ctx)