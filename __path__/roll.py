# Plugin permettant le roll de dés grâce à pyhedrals

import discord
from discord.ext import commands
import pyhedrals

class Roll(commands.Cog) :

    def __init__(self, bot) :
        self.bot = bot

    @commands.command(name="roll", usage = "!roll xdy + z", description = "Roll un nombre aléatoire")
    async def roll(self, ctx: commands.Context, *, roll: str) -> None:
        """
        roll un ou plusieurs dés
        """
        try:
            dice_roller = pyhedrals.DiceRoller(
                maxDice=100,
                maxSides=10000,
            )
            result = dice_roller.parse(roll)
            roll_message = f"\N{GAME DIE} {ctx.message.author.mention} a lancé {roll} et obtenu **{result.result}**"
            await ctx.send(roll_message)

        except (
            ValueError,
            NotImplementedError,
            pyhedrals.InvalidOperandsException,
            pyhedrals.SyntaxErrorException,
            pyhedrals.UnknownCharacterException,
        ) as exception:
            await ctx.send("Roll impossible, il va falloir tirer une carte")

async def setup(bot : commands.Bot) :
    await bot.add_cog(Roll(bot))
