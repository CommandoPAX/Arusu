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
        `2d20kh` - Roll 2d20, keep highest die (e.g. initiative advantage)
        `4d4!+2` - Roll 4d4, explode on any 4s, add 2 to result
        `4d6rdl` - Roll 4d6, reroll all 1s, then drop the lowest die
        `6d6c>4` - Roll 6d6, count all dice greater than 4 as successes
        `10d10r<=2kh6` - Roll 10d10, reroll all dice less than or equal to 2, then keep the highest 6 dice
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