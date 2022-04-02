from redbot.core import commands, Config
import discord
import time

class Rename(commands.Cog):
    """Vous permet de rename tout le monde"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=300920211119)
        default_guild = {
            "enabled" : False,
            "roles": [],
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def chaos(self, ctx):
        """Les commandes pour le Chaos"""
        pass

    @chaos.command()
    async def enable(self, ctx):
        """Active le plugin"""
        await self.config.guild(ctx.guild).enabled.set(True)
        await ctx.send(("Chaos activé"))

    @chaos.command()
    async def disable(self, ctx):
        """Désactive le plugin"""
        await self.config.guild(ctx.guild).enabled.set(False)
        await ctx.send(("Chaos désactivé"))

    @chaos.command()
    async def add(self, ctx, role : discord.Role):
        """Ajoute un role (pas touche si vous n'êtes pas Corusu)"""
        async with self.config.guild(ctx.guild).roles() as roles:
                if role.id in roles:
                    await ctx.send("Le role est déjà dans la liste")
                    return
                roles.append(role.id)
                await ctx.send(("{} ajouté à la liste").format(role.mention))

    @chaos.command()
    async def remove(self, ctx, role: discord.Role):
        """Enleve un role (pas touche si vous n'êtes pas Corusu)"""
        async with self.config.guild(ctx.guild).roles() as roles:
            if role.id not in roles:
                await ctx.send("Le role n'est pas dans la liste")
                return
            roles.remove(role.id)
            await ctx.send(("{} enlevé de la liste").format(role.mention))
    
    @chaos.command()
    async def list(self, ctx):
        """Liste tout les roles"""
        async with self.config.guild(ctx.guild).roles() as roles:
            if not roles:
                await ctx.send("Aucun role dans la liste")
                return
            role_mentions = [ctx.guild.get_role(role_id).mention for role_id in roles]
            await ctx.send(("Liste: {}").format(", ".join(role_mentions)))

    @chaos.command()
    async def activation(self, ctx):
        """Active le chaos"""
        member = ctx.message.author
        data = await self.config.guild(member.guild).all()
        if not data["enabled"]:
            return
        await member.add_roles(*[member.guild.get_role(role_id) for role_id in data["roles"]])
        await ctx.send("La gloire du LSMB est avec toi pour environ 2 minutes")
        time.sleep(120)
        await member.remove_roles(*[member.guild.get_role(role_id) for role_id in data["roles"]])
        await ctx.send("La gloire du LSMB est parti")
