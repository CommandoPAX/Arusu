# Handles creating, modifying and playing playlists

import asyncio
import functools
import itertools
import math
import random
import os
import time

import discord
import yt_dlp as youtube_dl 
from async_timeout import timeout
from discord.ext import commands

import subprocess
import shutil
import re
import json

from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed
from Core.file_manager import file_manager
from Cogs.music import * 

# Requirements : 
# - One playlist per person, entirely which can be modified at will
# - Allows to play music from their playlist directly from it
# - Can loop the playlist 
# - Can shuffle the playlist
# - Lists all music in a playlist
# - Default playlist if none specified

class Playlist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}
        self.CogName = "Playlist"
        self.config = ArusuConfig()
        
    @commands.command(name = "playlist_init", usage = "", description = "Creates the required files for the cog to work")
    @commands.has_permissions(manage_guild = True)
    async def playlist_init(self, ctx) :
        """ 
        Creates the required files and directories for the cog to work
        """
        await ctx.reply("Initializing cog")
        os.system(f"mkdir ./Data/Custom/{self.CogName}")
        await ctx.reply("Cog ready for usage")
    
    @commands.command(name = "add", usage = "[youtube link]", description ="Adds a youtube link to a playlist")
    async def playlist_append(self, ctx, link) : 
        try :
            if ctx.author.id not in self.config["Playlist_ID"] :
                file_manager.mk_custom(self.CogName, ctx.author.id)
            playlist_ = file_manager.load_custom(self.CogName, ctx.author.id)
            if "music_list" not in playlist_.keys() : 
                playlist_["music_list"] = []
            playlist_["music_list"].append(link)
            file_manager.update_custom(self.CogName, ctx.author.id, playlist_)
            await ctx.reply(f"{link} has been added to the playlist")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="guild_get_icon", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error sending the guild icon")
        
async def setup(bot):
    await bot.add_cog(Playlist(bot))