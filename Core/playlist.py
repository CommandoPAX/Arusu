# Plugin gérant les playlist

import discord
from discord.ext import commands
from yt_dlp import YoutubeDL as youtube_dl
import asyncio

# Erreur dans le processus pour load le plugin

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

#Need to find a way to bypass exception due to unavailable music

ytdl = youtube_dl(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class QueueManager() :
    def __init__(self) : 
        self.__queue = []
    
    async def play_queue(self, ctx, n) :
        try : 
            if n < len(self.__queue):
                player = await YTDLSource.from_url(self.__queue[n], loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after = self.play_queue(self, ctx, n+1))
                await ctx.send(f'Now playing: {player.title}')
            else : 
                await ctx.send("Problem with the n check")
        except : 
            await ctx.send("Problem playing the queue")

    async def add_queue(self, ctx, url) :
        self.__queue.append(url)
        await ctx.send(f"{url} has been added to the queue.")

    async def rm_queue(self, ctx, url) :
        for i in len(self.__queue) :
            if self.__queue[i] == url :
                del self.___queue[i]
                await ctx.send("Track has been removed from the queue")

    async def clear_queue(self, ctx) :
        self.__queue = []
    
class Playlist() :
    def __init__(self) :
        self.playlist = []
        self.playlistname = "Default Playlist"

    def add_music(self, ctx, url) :
        try :
            if url not in self.playlist :
                self.playlist.append(url)
            else :
                ctx.send("Track already in playlist") #Might cause a problem due to the lack of await
        except :
            print(f"Could not add music to {self.playlistname}")

    def remove_music(self, ctx, url) : 
        try :
            for i in len(self.queue) :
                if self.queue[i] == url :
                    del self.queue[i]
                    ctx.send("Track has been removed from the queue") #Might cause a problem due to the lack of await
        except :
            print(f"Could not remove track from {self.playlistname}")