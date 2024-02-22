# Handles the API connexions and chatting with users

import characterai
import os
import discord 
import asyncio
from discord.ext import commands
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class Guild_Manager(commands.Cog):
    """A really bad idea in its final form"""
    
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
        
    """Example code from the docs :
import asyncio
from characterai import PyAsyncCAI

async def main():
    client = PyAsyncCAI('TOKEN') #Secret value generated with an account

    char = input('Enter CHAR: ') #Can be found in the URL

    # Getting chat info
    chat = await client.chat.get_chat(char)

    participants = chat['participants']

    # In the list of "participants",
    # a character can be at zero or in the first place
    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    while True:
        message = input('You: ')

        data = await client.chat.send_message(
            chat['external_id'], tgt, message
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        print(f"{name}: {text}")

asyncio.run(main())
    """

async def setup(bot : commands.Bot) :
    await bot.add_cog(Guild_Manager(bot))
