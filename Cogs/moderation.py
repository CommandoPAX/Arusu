#Plugin qui permet de réaliser plusieurs actions de modérations
#Avec la contribution de @W1sh

import discord
from discord.ext import commands
from Core.config import ArusuConfig
from Core.ErrorHandler import LogError, ErrorEmbed

class Moderation(commands.Cog):
    """Useful moderation commands"""
    def __init__(self, bot):
        self.bot = bot
        self.CogName = "Moderation"
        self.config = ArusuConfig()
        
    @commands.command(name = "kick", usage = "[member ID or mention] [Raison]", description = "Kicks the submitted member")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.User = None, reasonmsg=None):
        """
        Kicks the submitted user.
        """
        try :
            if reasonmsg == None:
                reasonmsg = "Pas de raison donnée."
            if member == None :
                LogError(CogName=self.CogName, CogFunct="kick (no user)", Error= "No user found")
                await ErrorEmbed(ctx, Error="No user submitted", CustomMSG="Error finding the user")
                return
            await ctx.guild.kick(user = member, reason = reasonmsg)
            await ctx.channel.send(f"L'utilisateur {member.mention} a été kick. Raison : {reasonmsg}")
            LogError(CogName=self.CogName, CogFunct="kick (successful)", Error= f"Successfully kicked user {member.id}")

        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="kick", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG="Error kicking the user")
            
    @commands.command(name = "ban", usage = "[member ID or mention] [Raison]", description = "Bans the submitted member")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.User = None, reasonmsg=None):
        """
        Bans the submitted user.
        """
        try :
            if reasonmsg == None:
                reasonmsg = "Pas de raison donnée."
            if member == None :
                LogError(CogName=self.CogName, CogFunct="ban (no user)", Error= "No user found")
                await ErrorEmbed(ctx, Error="No user submitted", CustomMSG="Error finding the user")
                return
            await ctx.guild.ban(user = member, reason = reasonmsg) #Also clears messages from the last 24 hours
            await ctx.channel.send(f"L'utilisateur {member.mention} a été ban. Raison : {reasonmsg}")
            LogError(CogName=self.CogName, CogFunct="ban (successful)", Error= f"Successfully banned user {member.id}")

        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="ban", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG="Error banning the user")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Moderation(bot))