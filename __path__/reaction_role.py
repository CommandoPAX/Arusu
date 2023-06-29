# Plugin gérant le don de rôle par réactions.

import discord
from discord.ext import commands


class ReactionRole(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        super().__init__(*args, **kwargs)
        self.role_message_id = 0  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {}

    @commands.command(name= "add_emoji", usage = " [Emoji ID] [Role ID]", descritption = "Adds an emoji to the list of role reactions")
    @commands.is_owner()
    async def addemoji(self, ctx, EmojiID, RoleID) :
        """
        Adds an emoji to the list of role reactions
        """
        try :
            self.emoji_to_role[discord.PartialEmoji(id=EmojiID)] = RoleID
            await ctx.send("L'émoji a été ajouté comme role réactions.")
        except :
            await ctx.send("Could not add emoji to list")

    @commands.command(name = "del_emoji", usage = "[Emoji ID]", description = "Removes an emoji from reaction roles")
    @commands.is_owner()
    async def rmemoji(self, ctx, EmojiID) :
        """
        Removes an emoji from reaction roles
        """
        try : 
            del self.emoji_to_role[discord.PartialEmoji(id=EmojiID)]
            await ctx.send("Emoji deleted")
        except :
            await ctx.send("Emoji not in list")

    @commands.command(name = "set_message", usage = "[Message ID]", description = "Sets the message to be used as the role reaction message")
    @commands.is_owner()
    async def setmsg(self, ctx, MSGID) :
        """
        Sets the message to be used as the role reaction message
        """
        try :
            self.role_message_id = MSGID
            await ctx.send("Role message set to ", MSGID)
        except :
            await ctx.send("Could not set role message")

    ################################################################################################################################### 

    @commands.Cog.listener(name = "on_raw_reaction_add")
    async def ReactionRole_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    
    @commands.Cog.listener(name = "on_raw_reaction_remove")
    async def ReactionRole_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

async def setup(bot : commands.Bot) :
    await bot.add_cog(ReactionRole(bot))
