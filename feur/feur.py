from redbot.core import commands, Config
import discord
import re
from redbot.core.commands import Cog
from redbot.core.bot import Red

list = ["Quoi", "quoi"]

message = discord.Message

class Feur(commands.Cog):
    """Quoi ? Feur"""
    
    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, 4766951341)
        default_guild_settings = {
            "enabled" : False,
        }
        default_member_settings = {"filter_count": 0, "next_reset_time": 0}
        default_channel_settings = {"filter": []}
        self.config.register_guild(**default_guild_settings)
        self.config.register_member(**default_member_settings)
        self.config.register_channel(**default_channel_settings)
        self.pattern_cache = {}
        
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    
    @feurmain.command()
    async def enable(self, ctx):
        """Active le plugin"""
        await self.config.guild(ctx.guild).enabled.set(True)
        await ctx.send(("Feur activé"))
    
    @feurmain.command()
    async def disable(self, ctx):
        """Désactive le plugin"""
        await self.config.guild(ctx.guild).enabled.set(False)
        await ctx.send(("Feur désactivé"))
        
    @commands.Cog.listener()
    async def on_message(ctx, message):
        if "quoi" | "Quoi" in message.content.lower() :
            await ctx.send(("Feur"))
        else : 
            pass
        
