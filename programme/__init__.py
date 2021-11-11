from .mycog import Deck


def setup(bot):
    bot.add_cog(Deck(bot))
