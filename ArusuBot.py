from asyncio import AbstractEventLoop
from discord import Message
from discord.ext.commands import Bot, Context
from config import ArusuConfig


class Arusu(Bot):
    def __init__(self, listingSlash: bool = False, *args, **kwargs):
        """If listing Slash is False then the process is just a Player Process, should not interact with discord commands"""
        super().__init__(*args, **kwargs)
        self.__config = ArusuConfig()
        self.__listingSlash = listingSlash
        self.remove_command("help")

    @property
    def listingSlash(self) -> bool:
        return self.__listingSlash

    async def startBot(self):
        """Blocking function that will start the bot"""
        if self.__config.DATA["BOT_TOKEN"]== '':
            print('DEVELOPER NOTE -> Token not found')
            exit()

        await self.start(self.__config.DATA["BOT_TOKEN"], reconnect=True)

    async def startBotCoro(self, loop: AbstractEventLoop) -> None:
        """Start a bot coroutine, does not wait for connection to be established"""
        task = loop.create_task(self.__login())
        await task
        loop.create_task(self.__connect())

    async def __login(self):
        """Coroutine to login the Bot in discord"""
        await self.login(token=self.__config.DATA["BOT_TOKEN"])

    async def __connect(self):
        """Coroutine to connect the Bot in discord"""
        await self.connect(reconnect=True)

    async def process_commands(self, message: Message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=Context)

        if ctx.valid and not message.guild:
            return

        await self.invoke(ctx)
