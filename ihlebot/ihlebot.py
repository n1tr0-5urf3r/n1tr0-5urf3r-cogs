import discord
from discord.ext import commands
from .utils import checks
from cogs import * #dataIO, fileIO
from __main__ import send_cmd_help


import json
import os
import asyncio
import aiohttp
import datetime


class Ihlebot:
    """ Command definitions"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.session.close()

    @commands.group(pass_context=True)
    async def ihle(self, ctx):
        """First Test, Commandcall"""
        await self.bot.say('Ihle ist der beste!')

    @commands.command(pass_context=True)
    async def beleidige(self, ctx, name):
        """Second Test, Variablenverarbeitung"""
        msg = await self.bot.say(name + ' ist ein Behindi!')
        await self.add_reaction(msg, '\U0001F44D')

def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)