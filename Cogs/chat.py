import asyncio
import os
import pathlib
import spacy
from collections import defaultdict
from datetime import datetime, timedelta
from functools import partial
from typing import Dict, List, Optional
from config import ArusuConfig
from Core.ErrorHandler import LogError, ErrorEmbed
from Core.Predicate import MessagePredicate

import discord
from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.comparisons import JaccardSimilarity, LevenshteinDistance, SpacySimilarity
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer

#You will need to install these models manually

class FR_TRF:
    ISO_639_1 = "fr_dep_news_trf"
    ISO_639 = "fra"
    ENGLISH_NAME = "French"
    #python3 -m spacy download fr_dep_news_trf


class FR_LG:
    ISO_639_1 = "fr_core_news_lg" #500 MB
    ISO_639 = "fra"
    ENGLISH_NAME = "French"
    #python3 -m spacy download fr_core_news_lg 


class FR_MD:
    ISO_639_1 = "fr_core_news_md"
    ISO_639 = "fra"
    ENGLISH_NAME = "French"
    #python3 -m spacy download fr_core_news_md

class FR_SM:
    ISO_639_1 = "fr_core_news_sm"
    ISO_639 = "fra"
    ENGLISH_NAME = "French"
    #python3 -m spacy download fr_core_news_sm
    

class Chatter(commands.Cog):
    """
    This cog trains a chatbot that will talk like members of your Guild
    """
    models = [FR_MD, FR_LG, FR_TRF]
    algos = [SpacySimilarity, JaccardSimilarity, LevenshteinDistance]

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = ArusuConfig()
        path: pathlib.Path = pathlib.Path("ChatterData")
        self.data_path = path / pathlib.Path("database.sqlite3")
        if "model_number" in self.config.DATA.keys() :
            pass
        else : 
            self.config.update("model_number", 0)
            self.config.update("algo_number", 0)
            self.config.update("threshold", 0.90)
        self.similarity_algo = SpacySimilarity
        self.similarity_threshold = 0.90
        self.loop = asyncio.get_event_loop()
        self._last_message_per_channel: Dict[Optional[discord.Message]] = defaultdict(lambda: None)
        
    async def initialize(self):
            #TODO : Configure a base algo Number
            #TODO : Configure a base model number
            #TODO : Configure a base threshold
            model_number = self.config.DATA["model_number"]
            algo_number = self.config.DATA["algo_number"]
            threshold = self.config.DATA["threshold"]
            
            self.tagger_language = self.models[model_number]
            self.similarity_algo = self.algos[algo_number]
            self.similarity_threshold = threshold
            self.chatbot = self._create_chatbot()

    def _create_chatbot(self):

        return ChatBot(
            "ChatterBot",
            storage_adapter="Core.storage_adapters.MyDumbSQLStorageAdapter",
            database_uri="sqlite:///" + str(self.data_path),
            statement_comparison_function=self.similarity_algo,
            response_selection_method=get_random_response,
            logic_adapters=["chatterbot.logic.BestMatch"],
            maximum_similarity_threshold=self.similarity_threshold,
            tagger_language=self.tagger_language,
        )

    async def _get_conversation(self, ctx, in_channels: List[discord.TextChannel]):
        """
        Compiles all conversation in the Guild this bot can get it's hands on
        Currently takes a stupid long time
        Returns a list of text
        """
        out = [[]]
        after = datetime.today() - timedelta(days=(await self.config.guild(ctx.guild).days()))
        convo_delta = timedelta(minutes=(await self.config.guild(ctx.guild).convo_delta()))

        def predicate(msg: discord.Message):
            return msg.clean_content

        def new_conversation(msg, sent, out_in, delta):
            # Should always be positive numbers
            return msg.created_at - sent >= delta

        for channel in in_channels:
            # if in_channel:
            #     channel = in_channel
            await ctx.maybe_send_embed("Gathering {}".format(channel.mention))
            user = None
            i = 0
            send_time = after - timedelta(days=100)  # Makes the first message a new message

            try:

                async for message in channel.history(
                    limit=None, after=after, oldest_first=True
                ).filter(
                    predicate=predicate
                ):  # type: discord.Message
                    # if message.author.bot:  # Skip bot messages
                    #     continue
                    if new_conversation(message, send_time, out[i], convo_delta):
                        out.append([])
                        i += 1
                        user = None

                    send_time = (
                        message.created_at
                    )  # + timedelta(seconds=1)  # Can't remember why I added 1 second

                    if user == message.author:
                        out[i][-1] += "\n" + message.clean_content
                    else:
                        user = message.author
                        out[i].append(message.clean_content)

            except Exception as e :
                LogError("chat", "get_conversation", e)
                pass

        return out

    @commands.group(invoke_without_command=False)
    async def chatter(self, ctx: commands.Context):
        """
        Base command for this cog. Check help for the commands list.
        """
        self._guild_cache[ctx.guild.id] = {}  # Clear cache when modifying values
        self._global_cache = {}

    @commands.is_owner()
    @chatter.command(name="channel")
    async def chatter_channel(
        self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None
    ):
        """
        Set a channel that the bot will respond in without mentioning it

        Pass with no channel object to clear this guild's channel
        """
        if channel is None:
            await self.config.guild(ctx.guild).chatchannel.set(None)
            await ctx.maybe_send_embed("Chat channel for guild is cleared")
        else:
            if channel.guild != ctx.guild:
                await ctx.maybe_send_embed("What are you trying to pull here? :eyes:")
                return
            await self.config.guild(ctx.guild).chatchannel.set(channel.id)
            await ctx.maybe_send_embed(f"Chat channel is now {channel.mention}")

    @commands.is_owner()
    @chatter.command(name="reply")
    async def chatter_reply(self, ctx: commands.Context, toggle: Optional[bool] = None):
        """
        Toggle bot reply to messages if conversation continuity is not present

        """
        reply = await self.config.guild(ctx.guild).reply()
        if toggle is None:
            toggle = not reply
        await self.config.guild(ctx.guild).reply.set(toggle)

        if toggle:
            await ctx.maybe_send_embed(
                "I will now respond to you if conversation continuity is not present"
            )
        else:
            await ctx.maybe_send_embed(
                "I will not reply to your message if conversation continuity is not present, anymore"
            )

    @commands.is_owner()
    @chatter.command(name="learning")
    async def chatter_learning(self, ctx: commands.Context, toggle: Optional[bool] = None):
        """
        Toggle the bot learning from its conversations.

        This is a global setting.
        This is on by default.
        """
        learning = await self.config.learning()
        if toggle is None:
            toggle = not learning
        await self.config.learning.set(toggle)

        if toggle:
            await ctx.maybe_send_embed("I will now learn from conversations.")
        else:
            await ctx.maybe_send_embed("I will no longer learn from conversations.")

    @commands.is_owner()
    @chatter.command(name="cleardata")
    async def chatter_cleardata(self, ctx: commands.Context, confirm: bool = False):
        """
        This command will erase all training data and reset your configuration settings.

        This applies to all guilds.

        Use `[p]chatter cleardata True` to confirm.
        """

        if not confirm:
            await ctx.maybe_send_embed(
                "Warning, this command will erase all your training data and reset your configuration\n"
                "If you want to proceed, run the command again as `[p]chatter cleardata True`"
            )
            return
        async with ctx.typing():
            await self.config.clear_all()
            self.chatbot = None
            await asyncio.sleep(
                10
            )  # Pause to allow pending commands to complete before deleting sql data
            if os.path.isfile(self.data_path):
                try:
                    os.remove(self.data_path)
                except PermissionError:
                    await ctx.maybe_send_embed(
                        "Failed to clear training database. Please wait a bit and try again"
                    )

            self._create_chatbot()

        await ctx.tick()

    @commands.is_owner()
    @chatter.command(name="algorithm", aliases=["algo"])
    async def chatter_algorithm(
        self, ctx: commands.Context, algo_number: int, threshold: float = None
    ):
        """
        Switch the active logic algorithm to one of the three. Default is Spacy

        0: Spacy
        1: Jaccard
        2: Levenshtein
        """
        if algo_number < 0 or algo_number > 2:
            await ctx.send_help()
            return

        if threshold is not None:
            if threshold >= 1 or threshold <= 0:
                await ctx.maybe_send_embed(
                    "Threshold must be a number between 0 and 1 (exclusive)"
                )
                return
            else:
                self.similarity_threshold = threshold
                await self.config.threshold.set(self.similarity_threshold)

        self.similarity_algo = self.algos[algo_number]
        await self.config.algo_number.set(algo_number)

        async with ctx.typing():
            self.chatbot = self._create_chatbot()

            await ctx.tick()

    @commands.is_owner()
    @chatter.command(name="model")
    async def chatter_model(self, ctx: commands.Context, model_number: int):
        """
        Switch the active model to one of the three. Default is Small

        0: Small
        1: Medium (Requires additional setup)
        2: Large (Requires additional setup)
        3. Accurate (Requires additional setup)
        """
        if model_number < 0 or model_number > 3:
            await ctx.send_help()
            return

        if model_number >= 0:
            await ctx.maybe_send_embed(
                "Additional requirements needed. See guide before continuing.\n" "Continue?"
            )
            pred = MessagePredicate.yes_or_no(ctx)
            #Replace above function with a function that checks if the answer is a yes or no
            try:
                await self.bot.wait_for("message", check=pred, timeout=30)
            except TimeoutError:
                await ctx.send("Response timed out, please try again later.")
                return
            if not pred.result:
                return

        self.tagger_language = self.models[model_number]
        await self.config.model_number.set(model_number)
        async with ctx.typing():
            self.chatbot = self._create_chatbot()

            await ctx.maybe_send_embed(
                f"Model has been switched to {self.tagger_language.ISO_639_1}"
            )

    @commands.is_owner()
    @chatter.group(name="trainset")
    async def chatter_trainset(self, ctx: commands.Context):
        """Commands for configuring training"""
        pass

    @commands.is_owner()
    @chatter_trainset.command(name="minutes")
    async def minutes(self, ctx: commands.Context, minutes: int):
        """
        Sets the number of minutes the bot will consider a break in a conversation during training
        Active servers should set a lower number, while less active servers should have a higher number
        """

        if minutes < 1:
            await ctx.send_help()
            return

        await self.config.guild(ctx.guild).convo_delta.set(minutes)

        await ctx.tick()

    @commands.is_owner()
    @chatter_trainset.command(name="age")
    async def age(self, ctx: commands.Context, days: int):
        """
        Sets the number of days to look back
        Will train on 1 day otherwise
        """

        if days < 1:
            await ctx.send_help()
            return

        await self.config.guild(ctx.guild).days.set(days)
        await ctx.tick()

    @commands.is_owner()
    @chatter.command(name="backup")
    async def backup(self, ctx, backupname):
        """
        Backup your training data to a json for later use
        """

        await ctx.maybe_send_embed("Backing up data, this may take a while")

        path: pathlib.Path = pathlib.Path("ChatterData")

        trainer = ListTrainer(self.chatbot)

        future = await self.loop.run_in_executor(
            None, trainer.export_for_training, str(path / f"{backupname}.json")
        )

        if future:
            await ctx.maybe_send_embed(f"Backup successful! Look in {path} for your backup")
        else:
            await ctx.maybe_send_embed("Error occurred :(")

    @commands.is_owner()
    @chatter.group(name="train")
    async def chatter_train(self, ctx: commands.Context):
        """Commands for training the bot"""
        pass

    @chatter_train.command(name="channel")
    async def chatter_train_channel(
        self, ctx: commands.Context, channels: commands.Greedy[discord.TextChannel]
    ):
        """
        Trains the bot based on language in this guild.
        """
        if not channels:
            await ctx.send_help()
            return

        await ctx.maybe_send_embed(
            "Warning: The cog may use significant RAM or CPU if trained on large data sets.\n"
            "Additionally, large sets will use more disk space to save the trained data.\n\n"
            "If you experience issues, clear your trained data and train again on a smaller scope."
        )

        async with ctx.typing():
            conversation = await self._get_conversation(ctx, channels)

        if not conversation:
            await ctx.maybe_send_embed("Failed to gather training data")
            return

        await ctx.maybe_send_embed(
            "Gather successful! Training begins now\n"
            "(**This will take a long time, be patient. See console for progress**)"
        )
        embed = discord.Embed(title="Loading")
        embed.set_image(url="http://www.loop.universaleverything.com/animations/1295.gif")
        temp_message = await ctx.send(embed=embed)
        future = await self.loop.run_in_executor(None, self._train, conversation)

        try:
            await temp_message.delete()
        except discord.Forbidden:
            pass

        if future:
            await ctx.maybe_send_embed("Training successful!")
        else:
            await ctx.maybe_send_embed("Error occurred :(")

    ################################################################################################################################### 

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        """
        Credit to https://github.com/Twentysix26/26-Cogs/blob/master/cleverbot/cleverbot.py
        for on_message recognition of @bot

        Credit to:
        https://github.com/Cog-Creators/Red-DiscordBot/blob/V3/develop/redbot/cogs/customcom/customcom.py#L508
        for the message filtering
        """
        ###########

        if len(message.content) < 2 or message.author.bot:
            return

        guild: discord.Guild = getattr(message, "guild", None)

        if guild is None or await self.bot.cog_disabled_in_guild(self, guild):
            return

        ctx: commands.Context = await self.bot.get_context(message)

        if ctx.prefix is not None:  # Probably unnecessary, we're in on_message_without_command
            return

        ###########
        # Thank you Cog-Creators
        channel: discord.TextChannel = message.channel

        if not self._guild_cache[guild.id]:
            self._guild_cache[guild.id] = await self.config.guild(guild).all()

        is_reply = False  # this is only useful with in_response_to
        if (
            message.reference is not None
            and isinstance(message.reference.resolved, discord.Message)
            and message.reference.resolved.author.id == self.bot.user.id
        ):
            is_reply = True  # this is only useful with in_response_to
            pass  # this is a reply to the bot, good to go
        elif guild is not None and channel.id == self._guild_cache[guild.id]["chatchannel"]:
            pass  # good to go
        else:
            when_mentionables = commands.when_mentioned(self.bot, message)

            prefix = self.config.DATA["BOT_PREFIX"]

            if prefix is None:
                # print("not mentioned")
                return

            message.content = message.content.replace(prefix, "", 1)

        text = message.clean_content

        async with ctx.typing():

            if is_reply:
                in_response_to = message.reference.resolved.content
            elif self._last_message_per_channel[ctx.channel.id] is not None:
                last_m: discord.Message = self._last_message_per_channel[ctx.channel.id]
                minutes = self._guild_cache[ctx.guild.id]["convo_delta"]
                if (datetime.utcnow() - last_m.created_at).seconds > minutes * 60:
                    in_response_to = None
                else:
                    in_response_to = last_m.content
            else:
                in_response_to = None

            # Always use generate reponse
            # Chatterbot tries to learn based on the result it comes up with, which is dumb
            Statement = self.chatbot.storage.get_object("statement")
            future = await self.loop.run_in_executor(
                None, self.chatbot.generate_response, Statement(text)
            )

            if not self._global_cache:
                self._global_cache = await self.config.all()

            if in_response_to is not None and self._global_cache["learning"]:
                await self.loop.run_in_executor(
                    None,
                    partial(
                        self.chatbot.learn_response,
                        Statement(text),
                        previous_statement=in_response_to,
                    ),
                )

            replying = None
            if (
                "reply" not in self._guild_cache[guild.id] and self.default_guild["reply"]
            ) or self._guild_cache[guild.id]["reply"]:
                if message != ctx.channel.last_message:
                    replying = message

            if future and str(future):
                self._last_message_per_channel[ctx.channel.id] = await channel.send(
                    str(future), reference=replying
                )
            else:
                await ctx.send(":thinking:")
    
async def setup(bot : commands.Bot) :
    cog = Chatter(bot)
    await cog.initialize()
    await bot.add_cog(cog)