from .Chaos import Rename


def setup(bot):
    cog = Rename(bot)
    bot.add_cog(cog)