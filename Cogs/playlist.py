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
        
async def setup(bot):
    await bot.add_cog(Playlist(bot))