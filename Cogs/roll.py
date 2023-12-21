# Plugin permettant le roll de dés grâce à pyhedrals

import discord
from discord.ext import commands
import pyhedrals
from Core.error_handler import LogError, ErrorEmbed
from Cogs.deck import Deck

class Roll(commands.Cog) :
    """
    Rolls a dice
    """

    def __init__(self, bot) :
        self.bot = bot
        self.CogName = "Roll"

    @commands.command(name="roll", usage = "xdy + z", description = "Roll un nombre aléatoire")
    async def roll(self, ctx: commands.Context, *, roll: str) -> None:
        """
        roll un ou plusieurs dés
        """
        try:
            dice_roller = pyhedrals.DiceRoller()
            result = dice_roller.parse(roll)
            roll_message = f"\N{GAME DIE} {ctx.message.author.mention} a lancé {roll} et obtenu **{result.result}**"
            await ctx.send(roll_message)

        except Exception as e:
            LogError(CogName=self.CogName, CogFunct="roll", Error=e)
            await ErrorEmbed(ctx, Error=e, CustomMSG= "Error in rolling the dice, please draw a card from the deck")
            await Deck.drawmain(self, ctx, nb=1)

async def setup(bot : commands.Bot) :
    await bot.add_cog(Roll(bot))