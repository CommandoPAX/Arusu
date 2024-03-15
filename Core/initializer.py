from random import choices
import string
import discord

from Core.config import ArusuConfig
from Core.help import HelpCommand
from Core.bot import Arusu

class ArusuInit:
    def __init__(self, willListen: bool) -> None:
        self.__config = ArusuConfig()
        self.__intents = discord.Intents.all()
        self.__intents.message_content = True
        self.__intents.members = True
        self.__bot = self.__create_bot(willListen)

    def getBot(self):
        return self.__bot

    def __create_bot(self, willListen: bool):
        if willListen:
            prefix = self.__config["BOT_PREFIX"]
            bot = Arusu(listingSlash=False,
                            command_prefix=prefix,
                            pm_help=False,
                            case_insensitive=True,
                            intents=self.__intents)
            bot.help_command = HelpCommand()
        else:
            prefix = self.__config["BOT_PREFIX"]
            bot = Arusu(listingSlash=False,
                            command_prefix=prefix,
                            pm_help=False,
                            case_insensitive=True,
                            intents=self.__intents)
            bot.help_command = HelpCommand()
        return bot
