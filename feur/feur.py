from redbot.core import commands
import re

list = ["Quoi", "quoi"]

class Feur(commands.Cog):
    """Quoi ? Feur"""

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name = "feur", invoque_without_command = True)
    async def feurmain(self, ctx) :
        pass
    @feurmain.command(name = "activate")
    async def actimain(self, ctx) :
        activate = True
        if activate == True : 
            activate = False
            await ctx.send("Feur désactivé")
        else :
            activate = True
            await ctx.send("Feur activé")
     
    @feurmain.event
    async def on_message(message):
        if activate == True :
            for l in list :
                if re.search(l, message.content) :
                    await ctx.send("Feur")
                else : 
                    pass
        else :
            pass
    
    
