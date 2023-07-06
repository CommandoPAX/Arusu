# Plugin gérant l'audio

import asyncio
import discord
from yt_dlp import YoutubeDL as youtube_dl

#Install the following version
#pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"
#pip install yt_dlp

from discord.ext import commands
from Core.playlist import QueueManager, YTDLSource

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = QueueManager()
        self.repeat = False

    @commands.command(name = "join", usage = "", description = "Joins a voice channel")
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """
        Joins a voice channel
        """
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

    @commands.command(name = "dl_play", usage = "url", description = "Plays from a url (almost anything youtube_dl supports). Warning this downloads the music.")
    @commands.is_owner()
    async def download_play(self, ctx, url):
        """
        Plays from a url (almost anything youtube_dl supports). Warning this downloads the music.
        """
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

    @commands.command(name = "play", usage = "url", description = "Plays audio from youtube")
    async def play(self, ctx, url):
        """
        Plays audio from youtube
        """
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

    @commands.command(name = "play_wip", usage = "url", description = "Plays audio from youtube")
    @commands.is_owner()
    async def play_wip(self, ctx, url):
        """
        Plays audio from youtube (W.I.P. command using the queue system, not currently operationnal)
        """
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused :
            await self.queue.add_queue(self, ctx, url)
        else :
            self.queue.add_queue(self, ctx, url)
            if self.repeat == True :
                while self.repeat == True :
                    await self.queue.play_queue(self, ctx, 0)
            else : 
                await self.queue.play_queue(self, ctx, 0)

    @commands.command(name = "volume", usage = "percentage", description = "Changes the player's volume. Default is 50%")
    async def volume(self, ctx, volume: int):
        """
        Changes the player's volume. Default is 50%
        """
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name = "disconnect", usage = "", description = "Stops and disconnects the bot from voice", aliases = ["leave"])
    async def stop(self, ctx):
        """
        Stops and disconnects the bot from voice
        """
        await ctx.voice_client.disconnect()
    
    @commands.command(name = "repeat", usage = "", description = "Enables/disables repeating the queue")
    async def repeat_cmd(self, ctx) :
        """
        Enables/disables repeating the queue
        """
        if ctx.voice_client.is_playing() != True :
            await ctx.send("Bot not connected to a voice channel")
        else :
            if len(self.queue) == 0 :
                await ctx.send("Nothing in queue")
            if self.repeat == True : 
                self.repeat = False
                await ctx.send("Repeat disabled")
            if self.repeat == False :
                self.repeat = True
                await ctx.send("Repeat enabled")

    @commands.command(name = "remove_queue", usage = "url", description = "Removes an URL from the queue")
    async def remove_queue_cmd(self, ctx, url) :
        """
        Removes an URL from the queue
        """
        try :
            self.rm_queue(self, url)
            await ctx.send(f"{url} removed from queue")
        except :
            await ctx.send("Could not remove URL from queue")

    @commands.command(name = "clear_queue", usage = "", description = "Clears the queue")
    async def clear_queue(self, ctx) : 
        """
        Clears the queue
        """
        self.queue = {}
        await ctx.send("Queue cleared")

    @commands.command(name = "queue", usage = "", description = "Lists all elements in the queue")
    async def queue_list(self, ctx) :
        """
        Lists all elements in the queue
        """
        if len(self.queue) == 0 :
            await ctx.send("Queue is empty")
        else : 
            for i in range(len(self.queue)) : 
                await ctx.send(f"{self.queue[i]}\n")

    @commands.command(name = "next", usage = "", description = "plays the next music")
    async def nxtcmd(self, ctx) :
        """
        Plays the next music
        """
        pass

    @commands.command(name = "pause", usage = "", description = "Pauses the audio playing")
    async def pausecmd(self, ctx) : 
        """
        Pauses the audio playing
        """
        if ctx.voice_client.is_playing()  and ctx.voice_client.is_paused() != True :
            await ctx.voice_client.pause()
            await ctx.send("Audio paused")
        else :
            await ctx.send("Not currently playing audio")

    @commands.command(name = "resume", usage = "", description = "Resumes the audio playing")
    async def resumecmd(self, ctx) : 
        """
        Resumes the audio playing
        """
        if ctx.voice_client.is_paused() == True :
            await ctx.voice_client.resume()
            await ctx.send("Resumed playing audio")
        else :
            await ctx.send("Audio is already paused / No audio currently being played.")

    @commands.command(name ="stop", usage = "", description = "Stops playing the audio")
    async def stopcmd(self, ctx) :
        """
        Stops playing the audio
        """
        if ctx.voice_client.is_playing() == True or ctx.voice_client.is_paused() == True :
            await ctx.voice_client.stop()
            await ctx.send("Audio stopped")
        else :
            await ctx.send("Could not stop audio")

    @play.before_invoke
    @play_wip.before_invoke
    @download_play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Music(bot))
