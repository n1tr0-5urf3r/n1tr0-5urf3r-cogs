import discord
from discord.ext import commands
#from .utils import checks
from cogs import * #dataIO, fileIO
#from __main__ import send_cmd_help


import json
import os
import asyncio
import aiohttp
import datetime


class APIError(Exception):
    pass


class APIKeyError(Exception):
    pass

class Ihlebot:
    """ Command definitions"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.session.close()

    @commands.group(pass_context=True)
    async def ihle(self, ctx):
        """Erster Test, Commandaufruf"""
        self.bot.say('Ihle ist der beste!')

def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n._gamebuild_checker())
    bot.add_cog(n)