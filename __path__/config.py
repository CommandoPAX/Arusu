# Plugin gérant la config d'Arusu

import json
from discord.ext import commands, tasks
import os
from discord import Embed
from random import random
from datetime import timedelta

class ArusuConfig() : 
    def __init__(self) :
        self.BOT_PREFIX = '?'
        with open(r"C:\Users\bruan\Pictures\Bot Discord\ArusuDev\config.json", 'r') as f:
            self.DATA = json.load(f)
                
