class Deck(commands.Cog):
    """Deck des catastrophes"""

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name = "deck", invoque_without_command = True)
    async def deckmain(self, ctx): #tire une carte tout le temps, commande à redef
        pass
    
    @deckmain.command(name = "draw")
    async def drawmain(self, ctx):
        """Tire une carte du deck des catastrophes"""
        carte = random.choice(tuple(CarteDeck.keys()))
        Rep = "Vous avez tiré la carte : " + str(carte)
        await ctx.send(Rep)

    @deckmain.command(name = "effet")
    async def effetmain(self, ctx, Carte2):
        """Donne l'effet d'une carte du deck. Le nom de la carte doit être entre guillemet."""
        if Carte2 in CarteDeck : 
            Rep = CarteDeck[Carte2]
            Rep2 = str(Carte2)+ " : " + str(Rep)
            await ctx.send(Rep2)
        else :
            await ctx.send("Le nom de la carte est invalide.")
    
    @deckmain.command(name = "list") #Ne marche pas, surement à cause de la limite de message de discord
    async def listmain(self, ctx):
        """Liste l'intégralité des cartes du deck ainsi que leur effet."""
        await ctx.send("Liste des effets du deck : \n") 
        Rep3 = ""
        for i, j in CarteDeck.items() :
            Rep3 = Rep3 + str(i) + " : " + str(j) + "\n"
            if len(Rep3) >= 1500 :
                await ctx.send(Rep3)
                Rep3 = ""
        await ctx.send(Rep3)
        
    @deckmain.command(name = "nombre")
    async def nombremain(self, ctx):
       """Donne le nombre de carte dans le deck"""
       n = int(len(CarteDeck))
       await ctx.send(n)
