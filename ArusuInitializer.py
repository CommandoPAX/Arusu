from random import choices
import string
import discord
import os
from discord.ext import commands
from os import listdir
from ArusuBot import Arusu
from __path__.config import ArusuConfig
from help import HelpCommand

class ArusuInit:
    def __init__(self, willListen: bool) -> None:
        self.__config = ArusuConfig()
        self.__intents = discord.Intents.all()
        self.__intents.message_content = True
        self.__intents.members = True
        self.__bot = self.__create_bot(willListen)
        #self.__add_cogs(self.__bot)

    def getBot(self):
        return self.__bot

    def __create_bot(self, willListen: bool):
        if willListen:
            prefix = self.__config.DATA["BOT_PREFIX"]
            bot = Arusu(listingSlash=False,
                            command_prefix=prefix,
                            pm_help=False,
                            case_insensitive=True,
                            intents=self.__intents)
            bot.help_command = HelpCommand()
        else:
            prefix = ''.join(choices(string.ascii_uppercase + string.digits, k=4))
            bot = Arusu(listingSlash=False,
                            command_prefix=prefix,
                            pm_help=False,
                            case_insensitive=True,
                            intents=self.__intents)
            bot.help_command = HelpCommand()
        return bot