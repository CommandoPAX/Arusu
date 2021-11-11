from redbot.core import commands

Programme = "1. Bannir Pepsire" \n "2. Réduire la présence des fumos sur le serveur" \n "3. Tout le monde devra tirer une carte du deck chaque jour" \n "4. Le salaire quotidien sera augmenté de 5 Arucoins." \n "5. Cette augmentation sera financé en taxant K.N.G." \n "6. La Corée du Nord sera envahie et éradiquée pour la gloire d'Arusu" \n "7. Des cours de fuséologie seront accessibles à tout le monde et ce gratuitement." \n "8. Le only-fan de Janirf sera en accès libre pour l'intégralité des membres du LSMB."  

class Deck(commands.Cog):
    """Programme présidentielle"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deck(self, ctx):
        """Donne le programme officiel d'Arusu pour la présidentielle de 2022"""
        await ctx.send(Programme)
