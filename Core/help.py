# Commande d'aide d'Arusu

from discord.ext import commands
import discord
from config import ArusuConfig
from Core.ErrorHandler import LogError

class HelpCommand(commands.HelpCommand):
    
    def get_command_signature(self, command):
        return f"{command.qualified_name} {command.signature} : {command.description}" #The line to modify to include / excluse information from the help command
        #Right now it shows : <prefix>CommandName CommandArgs
        
    ################################################################################################################################### 
    #Gets called with <prefix>help
    
    async def send_bot_help(self, mapping):
        try :
            self.config = ArusuConfig()
            embed = discord.Embed(title="Help", color=discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"])) #Creates the embed
            
            for cog, commands in mapping.items(): #mapping.items() returns a list of tuple (Cog, [commands])
                filtered = await self.filter_commands(commands, sort=True)
                if command_signatures := [
                    self.get_command_signature(c) for c in filtered #calls the function we defined above to return the list of parameters
                ]:
                    cog_name = getattr(cog, "qualified_name", "No Category") #This gets the cog's name or return "No Category if it's not found"
                    embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False) 

            channel = self.get_destination()
            await channel.send(embed=embed)
        except Exception as e:
            LogError(CogName="HelpCommand", CogFunct="send_bot_help", Error=e)

    ################################################################################################################################### 
    #Gets called with <prefix>help <command>
    
    async def send_command_help(self, command):
        try :
            self.config = ArusuConfig()
            embed = discord.Embed(title=self.get_command_signature(command) , color=discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"]))
            
            if command.help: #Returns the help of a command found in the docstrings
                embed.description = command.help
            if alias := command.aliases: #Returns the aliases for the command if they exist
                embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)
        except Exception as e:
            LogError(CogName="HelpCommand", CogFunct="send_command_help", Error=e)

    ################################################################################################################################### 
    #Gets called with <prefix>help <group>

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        try :
            self.config = ArusuConfig()
            embed = discord.Embed(title=title, description=description or "No help found...", color=discord.Color.from_str(self.config.DATA["BOT_EMBED_COLOUR"]))

            if filtered_commands := await self.filter_commands(commands):
                for command in filtered_commands:
                    embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")

            await self.get_destination().send(embed=embed)
        except Exception as e:
            LogError(CogName="HelpCommand", CogFunct="send_help_embed", Error=e)

    async def send_group_help(self, group):
        try :
            self.config = ArusuConfig()
            title = self.get_command_signature(group)
            await self.send_help_embed(title, group.help, group.commands)
        except Exception as e:
            LogError(CogName="HelpCommand", CogFunct="send_group_help", Error=e)

    ################################################################################################################################### 
    #Gets called with <prefix>help <cog>

    async def send_cog_help(self, cog):
        try :
            self.config = ArusuConfig()
            title = cog.qualified_name or "No"
            await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        except Exception as e:
            LogError(CogName="HelpCommand", CogFunct="send_cog_help", Error=e)