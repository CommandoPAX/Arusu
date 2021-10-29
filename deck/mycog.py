from redbot.core import commands
import random

deck = ["Tu as tiré la carte : Balance", "Tu as tiré la carte : Comète", "Tu as tiré la carte : Donjon", "Tu as tiré la carte : Général Puzzle", "Tu as tiré la carte : Destin", "Tu as tiré la carte : Feu", "Tu as tiré la carte : Idiot", "Tu as tiré la carte : Gemme", "Tu as tiré la carte : Joker", "Tu as tiré la carte : Voyage astral à sens unique", "Tu as tiré la carte : Soldat", "Tu as tiré la carte : Lune", "Tu as tiré la carte : Ruine", "Tu as tiré la carte : Mort", "Tu as tiré la carte : Etoile", "Tu as tiré la carte : Soleil", "Tu as tiré la carte : Terre", "Tu as tiré la carte : Trône", "Tu as tiré la carte : Vizier", "Tu as tiré la carte : Vide", "Tu as tiré la carte : Animal", "Tu as tiré la carte : Cilmatosceptique", "Tu as tiré la carte : Dés", "Tu as tiré la carte : Voyage", "Tu as tiré la carte : Ombre", "Tu as tiré la carte : Magicien", "Tu as tiré la carte : Roue", "Tu as tiré la carte : Loto", "Tu as tiré la carte : Expérience", "Tu as tiré la carte : Hiérophante", "Tu as tiré la carte : Les Amoureux", "Tu as tiré la carte : Monde", "Tu as tiré la carte : Temps", "Tu as tiré la carte : Equilibre", "Tu as tiré la carte : Ambivalent", "Tu as tiré la carte : Sangsue", "Tu as tiré la carte : Faiblesse", "Tu as tiré la carte : Traitrise", "Tu as tiré la carte : Grande Prêtresse", "Tu as tiré la carte : Doppelganger", "Tu as tiré la carte : Explosion", "Tu as tiré la carte : Pigeon", "Tu as tiré la carte : Glace", "Tu as tiré la carte : Impératrice", "Tu as tiré la carte : Empereur", "Tu as tiré la carte : Chariot", "Tu as tiré la carte : Force", "Tu as tiré la carte : Hermite", "Tu as tiré la carte : Pendu", "Tu as tiré la carte : Tempérance", "Tu as tiré la carte : Diable", "Tu as tiré la carte : Jugement", "Tu as tiré la carte : Epée", "Tu as tiré la carte : Aléatoire", "Tu as tiré la carte : Pentacle", "Tu as tiré la carte : Dague", "Tu as tiré la carte : Oubli", "Tu as tiré la carte : Vision", "Tu as tiré la carte : Chaos", "Tu as tiré la carte : Baleine", "Tu as tiré la carte : Agilité", "Tu as tiré la carte : Thanos", "Tu as tiré la carte : LSMB", "Tu as tiré la carte : Trou noir", "Tu as tiré la carte : Ecureuil", "Tu as tiré la carte : Jouvence", "Tu as tiré la carte : Stop"]

class Deck(commands.Cog):
    """Deck des catastrophes"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deck(self, ctx):
        """Tire une carte du deck des catastrophes"""
        await ctx.send(random.choice(deck))
