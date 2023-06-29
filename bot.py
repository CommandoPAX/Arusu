#Core d'Arusu

import os
import discord
import asyncio
from discord.ext import commands

TOKEN = "TOKEN"

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all()) #set le prefix et les intents

async def load() :
    for root,dirs,files in os.walk("./__path__"): #check le dossier plugins pour chaque fichier
        for filename in files : 
            if filename.endswith(".py"): #sinon c'est pas des modules
                try : 
                    await bot.load_extension(f"__path__.{filename[:-3]}") #ajoute le module au bot
                except Exception as e:
                    print("Extension not loaded : ", filename, "\n")
                    print(e)
    try : 
        await bot.load_extension(f"__path__.chatter.chat")
    except :
        print("Chatter n'a pas pu être load")
        #print(Exception)
    
class SupremeHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blurple())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if command_signatures := [
                self.get_command_signature(c) for c in filtered
            ]:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command) , color=discord.Color.blurple())
        if command.help:
            embed.description = command.help
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = discord.Embed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()

        await channel.send(embed=embed)

bot.help_command = SupremeHelpCommand()

async def main(): #fonction qui load les modules et démarre le bot
    await load()
    await bot.start(TOKEN) #démarre le bot

asyncio.run(main())
