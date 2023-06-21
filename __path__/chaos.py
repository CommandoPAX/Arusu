import discord
from discord.ext import commands
import time
from datetime import datetime, timedelta, timezone
import asyncio

class Chaos(commands.Cog):
    """Vous permet de rename tout le monde"""

    def __init__(self, bot):
        self.bot = bot
        self.chaoswitch = True
        self.roles = []

    @commands.group()
    async def chaos(self, ctx):
        """Les commandes pour le Chaos"""
        pass

    @chaos.command(name = "enable", usage = "", description = "Active le plugin")
    @commands.is_owner()
    async def enable(self, ctx):
        """Active le plugin"""
        if self.chaoswitch == True :
            await ctx.send("Le chaos était déjà présent dans cet univers.")
        else : 
            self.chaoswitch = True
            await ctx.send(("Chaos activé"))

    @chaos.command()
    @commands.is_owner()
    async def disable(self, ctx):
        """Désactive le plugin"""
        if self.chaoswitch == False :
            await ctx.send("Le chaos avait déjà disparu, quelle tristesse.")
        else : 
            self.chaoswitch = False
            await ctx.send(("Chaos désactivé"))

    @chaos.command()
    @commands.is_owner()
    async def add(self, ctx, role : discord.Role):
        """Ajoute un role"""
        async with self.roles as roles:
            if role.id in roles:
                await ctx.send("Le role est déjà dans la liste")
                return
            roles.append(role.id)
            await ctx.send(("{} ajouté à la liste").format(role.mention))

    @chaos.command()
    @commands.is_owner()
    async def remove(self, ctx, role: discord.Role):
        """Enleve un role"""
        async with self.roles as roles:
            if role.id not in roles:
                await ctx.send("Le role n'est pas dans la liste")
                return
            roles.remove(role.id)
            await ctx.send(("{} enlevé de la liste").format(role.mention))
    
    @chaos.command()
    @commands.is_owner()
    async def list(self, ctx):
        """Liste tout les roles"""
        async with self.roles as roles:
            if not roles:
                await ctx.send("Aucun role dans la liste")
                return
            role_mentions = [ctx.guild.get_role(role_id).mention for role_id in roles]
            await ctx.send(("Liste: {}").format(", ".join(role_mentions)))

    @chaos.command()
    async def activate(self, ctx):
        """Active le chaos"""
        try :
            message = ctx.message
            await message.delete()
            member = ctx.message.author
            if self.chaoswitch != True :
                return
            await member.add_roles(*[member.guild.get_role(role_id) for role_id in self.roles])
            await asyncio.sleep(120)
            await member.remove_roles(*[member.guild.get_role(role_id) for role_id in self.roles])
        except Exception as e :
            await ctx.send("Le chaos n'a pas pu être activé.")
            print(e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(Chaos(bot))