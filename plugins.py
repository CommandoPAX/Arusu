# Ne va surement plus être utile a cause de changement dans le core

import importlib
from discord.ext import commands
import discord
plugins = {}

class PluginManager(commands.Cog) :
    def __init__(self, bot):
        self.bot = bot
        
    def setup(bot) : 
        bot.add_cog(PluginManager(bot))
        
    @commands.command()
    async def load(self, ctx, TBL) :
        try :
            await self.bot.load(TBL) 
        except :
            await ctx.send("Unable to load cog")
            
    @commands.command()
    async def unload(self, ctx, TBUL) : 
        try :
            await self.bot.unload(TBUL)
        except :
            await ctx.send("Unable to unload cog")
            
    '''@commands.command()
    async def importall():
        for cog in plugins.index() :
            importlib.import_module(name = plugins[cog])
        
    @commands.command()  
    async def addcog(cogname) : 
        plugins[cogname] = "./plugins/" + cogname
        
    @commands.command()
    async def rmcog(cogname) : 
        del plugins[cogname]'''
