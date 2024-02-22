# Handles the API connexions and chatting with users

from characterai import PyCAI
import random 
from discord.ext import commands
from Core.config import ArusuConfig
from Core.error_handler import LogError, ErrorEmbed

class AI(commands.Cog):
    """
    Arusu's AI, powered by CharacterAI.
    A version independent of outside API will be implemented someday.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "AI"
        self.config = ArusuConfig()
        try : 
            self.client = PyCAI(self.config.DATA["CAI_TOKEN"]) #Secret value generated with an account
            self.char = self.config.DATA["CAI_CHAR"] #Can be found in the URL
            
            # Getting chat info
            self.chat = self.client.chat.get_chat(self.char)

            self.participants = self.chat['participants']

            # In the list of "participants",
            # a character can be at zero or in the first place
            if not self.participants[0]['is_human']:
                self.tgt = self.participants[0]['user']['username']
            else:
                self.tgt = self.participants[1]['user']['username']
        except Exception as e : 
            LogError(self.CogName, "__init__", e)
        
    @commands.command(name = "character", usage = "[character ID]", description = "Changes the character")
    @commands.has_permissions(manage_guild = True)
    async def character_update(self, ctx, char_id : str) :
        """ 
        Changes the character 
        """
        try :
            self.config.update("CAI_CHAR", char_id)
            await ctx.send(f"Character has been changed, please restart the bot.")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="character_update", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not change character ID")
    
    @commands.command(name = "channel", usage = "[channel ID]", description = "Sets the channel in which the character will interact freely")
    @commands.has_permissions(manage_guild = True)
    async def set_main_channel(self, ctx, channel_id : int) :
        """ 
        Sets the channel in which the character will interact freely
        """
        try :
            self.config.update(f"{ctx.guild.id}.AIChannel", self.bot.get_channel(channel_id).id)
            await ctx.send(f"Welcome channel set to {self.config.DATA[f'{ctx.guild.id}.AIChannel']}")
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="set_main_channel", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Could not set main AI channel")

    @commands.command(name = "activate", usage = "", description = "Toggles the bot's AI on the guild")
    @commands.has_permissions(manage_guild = True)
    async def activate_AI(self, ctx) :
        """ 
        Activate or deactivate the bot's AI on the guild
        """
        try :
            if self.config.DATA[f"{ctx.guild.id}.CAIEnabled"] == False : 
                self.config.update(f"{ctx.guild.id}.CAIEnabled", True)
                await ctx.send("AI has been enabled on this server")
            elif self.config.DATA[f"{ctx.guild.id}.CAIEnabled"] == True : 
                self.config.update(f"{ctx.guild.id}.CAIEnabled", False)
                await ctx.send("AI has been disabled on this server")
        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="enable", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error enabling the cog")

    ################################################################################################################################### 

    @commands.Cog.listener(name = "on_message")
    async def AIAnswer(self, message):
        try :
            if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
                return
            if self.config.DATA[f"{message.guild.id}.CAIEnabled"] != True : 
                return
            if message.channel != self.config.DATA[f"{message.guild.id}.AIChannel"] : 
                if random.randint(1,200) != 1 :
                    if self.bot.user.id in message.content : 
                        pass 
                    else : 
                        return
                else : pass 
            
            data = await self.client.chat.send_message(
                self.chat['external_id'], self.tgt, message.content)

            text = data['replies'][0]['text']
            await message.reply(text)
            
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="listener", Error=e)
            await ErrorEmbed(message.channel, e, "Arusu bugged out, sad")
            self.config.update(f"{message.guild.id}.CAIEnabled", False) #Disables the plugin after an error to avoid spamming the logs
            pass

async def setup(bot : commands.Bot) :
    await bot.add_cog(AI(bot))
