# Plugin contenant l'autoroler ainsi que le selfrole

import discord
from discord.ext import commands

class autoroler(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot
        self.selfrolelist = []
        self.autorolelist = []
    
    @commands.command(name = "autorole_add", usage = "[Role ID]", description = "Sets a role to be given to new members")
    @commands.is_owner()
    async def autoroleadd(self, ctx, autoroleID) :
        """
        Add a role to be given to new members
        """
        try :
            if autoroleID not in self.autorolelist :
                self.autorolelist.append(autoroleID)
                await ctx.send("{} a été ajouté à l'autoroler.".format(autoroleID.mention))
            else : 
                await ctx.send("Le rôle était déjà dans la liste")
        except Exception as e :
            await ctx.send("Could not add role to list")
            print(e)

    @commands.command(name = "autorole_remove", usage = "[Role ID]", description = "Sets a role to be given to new members")
    @commands.is_owner()
    async def autoroleremove(self, ctx, autoroleID) :
        """
        Remove a role to be given to new members
        """
        try :
            if autoroleID in self.autorolelist :
                self.autorolelist.remove(autoroleID)
                await ctx.send("{} a été supprimé à l'autoroler.".format(autoroleID.mention))
            else : 
                await ctx.send("Le rôle n'était pas dans la liste")
        except Exception as e :
            await ctx.send("Could not remove role from list")
            print(e)
    
    @commands.command(name = "selfrole_add", usage = "[Role ID]", description = "Sets a new selfrole")
    @commands.is_owner()
    async def selfroleadd(self, ctx, selfroleID) :
        """
        Adds a selfrole
        """
        try :
            if selfroleID not in self.selfrolelist :
                self.selfrolelist.add(selfroleID)
                await ctx.send("{} a été ajouté en tant que selfrole.".format(selfroleID.mention))
            else : 
                await ctx.send("Le rôle était déjà dans la liste")
        except Exception as e :
            await ctx.send("Could not add role to list")
            print(e)

    @commands.command(name = "selfrole_remove", usage = "[Role ID]", description = "Removes a selfrole")
    @commands.is_owner()
    async def selfroleremove(self, ctx, selfroleID) :
        """
        Removes a selfrole
        """
        try :
            if selfroleID in self.selfrolelist :
                self.selfrolelist.remove(selfroleID)
                await ctx.send("{} a été enlevé de la liste.".format(selfroleID.mention))
            else : 
                await ctx.send("Le rôle n'était pas dans la liste")
        except Exception as e :
            await ctx.send("Could not remove role from list")
            print(e)

    @commands.command(name = "selfrole", usage = "[Role ID]", description = "Gives the member a selfrole")
    @commands.is_owner()
    async def selfrole(self, ctx, selfroleID) :
        """
        Gives the member a selfrole
        """
        try :
            if selfroleID in self.selfrolelist :
                await ctx.member.add_role(selfroleID)
                await ctx.send("Le rôle a été ajouté.")
            else : 
                await ctx.send("Le rôle n'est pas disponible.")
        except Exception as e :
            await ctx.send("Could not give role")
            print(e)

    ###################################################################################################################################

    @commands.Cog.listener(name = "on_member_join")
    async def autorole_member_join(self, member) :
        try : 
            await member.add_role(*[role_id for role_id in self.autorolelist])
        except Exception as e :
            print(e)

async def setup(bot : commands.Bot) :
    await bot.add_cog(autoroler(bot))
