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
        
    #Embed for the card list
    def create_embed_list(self, Playlist_ : dict, page : int = 1):
        
        self.items_per_page = 20
        self.pages = math.ceil(int(len(Playlist_["music_list"])) / self.items_per_page)

        start = (page - 1) * self.items_per_page
        end = start + self.items_per_page
        
        try :
            List = ""
            j = 1
            try :
                for i, link in enumerate(Playlist_[start:end], start=start):
                    List += f"**{j}.** {link} \n"
            except Exception as e :
                LogError(CogName=self.CogName, CogFunct="create_embed_list", Error=e)

            embed = (discord.Embed(title="Deck des catastrophes",
                                description=List,
                                color = discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])).set_footer(text=f"Page {page}/{self.pages}"))
            
            embed_list = []
            for i in range(self.pages) :
                Emb = self.create_embed_list(page=i+1)
                embed_list.append(Emb)
            return embed_list
            
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="create_embed_list", Error=e)
        
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
        """ 
        Adds a youtube link to a playlist
        """
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
            LogError(CogName=self.CogName, CogFunct="playlist_append", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error adding a music to the playlist")
            
    @commands.command(name = "remove", usage = "[youtube link]", description ="Removes a youtube link to a playlist")
    async def playlist_remove(self, ctx, link) : 
        """ 
        Removes a youtube link to a playlist
        """
        try :
            if ctx.author.id not in self.config["Playlist_ID"] :
                await ctx.reply("You don't have any playlist")
                return
            playlist_ = file_manager.load_custom(self.CogName, ctx.author.id)
            if link not in playlist_["music_list"] : 
                await ctx.reply("Couldn't find the corresponding track")
                return
            playlist_["music_list"] = playlist_["music_list"].remove(link)
            file_manager.update_custom(self.CogName, ctx.author.id, playlist_)
            await ctx.reply(f"{link} has been removed from the playlist")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="playlist_remove", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error removing the music from the playlist")
            
    @commands.command(name = "list", usgae = "", description = "Lists all music from a playlist")
    async def playlist_list(self, ctx) : 
        """ 
        Not currently functionnal
        """
        for element in self.Deck.list() :
            await ctx.send(embed = element)
        
async def setup(bot):
    await bot.add_cog(Playlist(bot))