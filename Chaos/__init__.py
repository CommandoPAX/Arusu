from .Chaos import Chaos


def setup(bot):
    cog = Rename(bot)
    bot.add_cog(cog)
