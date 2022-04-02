from .Chaos import Chaos


def setup(bot):
    cog = Chaos(bot)
    bot.add_cog(cog)
