import os
import discord
import asyncio
from discord.ext import commands

TOKEN = "TOKEN"

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

async def load() :
    for filename in os.listdir("./plugins"):
        if filename.endswith(".py"):
            await bot.load_extension(f"plugins.{filename[:-3]}")

async def main():
    await load()
    await bot.run(TOKEN)

asyncio.run(main())

@bot.event
async def on_ready():
    print("Hello world")
