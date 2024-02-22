# Handles the API connexions and chatting with users

from characterai import PyCAI
import random 
import discord
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
            
    def Answer(self, message_r : str) :
        try : 
            client = PyCAI(self.config.DATA["CAI_TOKEN"]) #Secret value generated with an account
            char = self.config.DATA["CAI_CHAR"] #Can be found in the URL
            
            # Getting chat info
            chat = client.chat.get_chat(char)

            participants = chat['participants']

            # In the list of "participants",
            # a character can be at zero or in the first place
            if not participants[0]['is_human']:
                tgt = participants[0]['user']['username']
            else:
                tgt = participants[1]['user']['username']
                
            data = client.chat.send_message(chat['external_id'], tgt, message_r)

            text = data['replies'][0]['text']
            return text
            
        except Exception as e : 
            LogError(self.CogName, "Answer", e)
        
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
            await ctx.send(f"AI channel set to {self.config.DATA[f'{ctx.guild.id}.AIChannel']}")
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
    async def AIAnswer(self, message : discord.Message):
        try :
            n = random.randint(1, 200) #Probability of the bot responding to a random message
            
            if message.author.id == self.bot.user.id:  #Stopping the bot from reading its own message
                return
            if self.config.DATA[f"{message.guild.id}.CAIEnabled"] != True : 
                return
            if message.content.startswith(self.config.DATA["BOT_PREFIX"]) : 
                return
            try :
                if message.channel.id != self.config.DATA[f"{message.guild.id}.AIChannel"] and n != 1 : 
                    if str(self.bot.user.id) not in message.content : 
                        return 
                else : 
                    pass 
            except : 
                self.config.update(f"{message.guild.id}.AIChannel", 0) #Disables the plugin after an error to avoid spamming the logs
                pass
            async with message.channel.typing():
                await message.reply(self.Answer(message.content))
            
        except Exception as e :
            LogError(CogName=self.CogName, CogFunct="listener", Error=e)
            await ErrorEmbed(message.channel, e, "Arusu bugged out, sad")
            self.config.update(f"{message.guild.id}.CAIEnabled", False) #Disables the plugin after an error to avoid spamming the logs
            pass

async def setup(bot : commands.Bot) :
    await bot.add_cog(AI(bot))
