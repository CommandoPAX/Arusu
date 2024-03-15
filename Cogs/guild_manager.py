# Allows everyone to interface with the guild management screen

import discord
import uuid
import requests
import shutil
import os
from discord.ext import commands
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Guild_Manager(commands.Cog):
    """A really bad idea in progress"""
    
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "Guild_Manager"
        self.config = ArusuConfig()
        
    @commands.command(name = "guild_init", usage = "", description = "Creates the required files for the cog to work")
    @commands.has_permissions(manage_guild = True)
    async def guild_init(self, ctx) :
        """ 
        Creates the required files and directories for the cog to work
        """
        await ctx.reply("Initializing cog")
        os.system(f"mkdir ./Data/Custom/{self.CogName}")
        await ctx.reply("Cog ready for usage")
         
    @commands.command(name = "icon", usage = "", description = "Changes the guild's logo")
    async def guild_logo(self, ctx):
        """
        Changes the guild's logo with a user submitted image
        """
        try :
            await ctx.reply("Trying to update guild icon")
            file_path = "./Data/Custom/" + self.CogName + "/"
            try :
                old_id = self.config[f"{ctx.guild.id}.IconName"]
                os.system(f"rm {file_path + old_id}")           # deletes the old file to avoid cluttering disk space
            except : 
                pass
            
            try:
                url = ctx.message.attachments[0].url            # check for an image, call exception if none found
            except IndexError:
                print("Error: No attachments")
                await ctx.send("No attachments detected!")
            else:
                if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
                    r = requests.get(url, stream=True)
                    imageName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
                    self.config.update(f"{ctx.guild.id}.IconName", imageName)
                    path = file_path + imageName
                    with open(path, 'wb') as out_file:
                        print('Saving image: ' + imageName)
                        shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)
                    
                    with open(path, "rb") as file:              # opens the file as a binary file, which is required by guild.edit
                        icon: bytes = file.read()
                        await ctx.guild.edit(icon=icon)
                    await ctx.send(f"Guild icon changed successfully")
                    
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="guild_logo", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error changing the guild icon")
            
    @commands.command(name = "get_icon", usage = "", description = "Returns the guild's icon")
    async def guild_get_icon(self, ctx):
        """
        Returns the guild's icon
        """
        try :
            file_path = "./Data/Custom/" + self.CogName + "/"
            id = self.config[f"{ctx.guild.id}.IconName"]
            path = file_path + id 
            
            with open(path, "rb") as f : 
                _file = discord.File(f)
            await ctx.reply("Here is the guild icon :", file = _file)
            
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="guild_get_icon", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error sending the guild icon")


async def setup(bot : commands.Bot) :
    await bot.add_cog(Guild_Manager(bot))
