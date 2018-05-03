# Discord stuff
import discord
import asyncio
import aiohttp
from discord.ext import commands



class UniBot:
    """ Command definitions"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.session.close()


    @commands.command(pass_context=True)
    async def testclass(self, ctx):
        """First Test, Commandcall"""
        await self.bot.say('Test funktioniert')


def setup(bot):
    n = UniBot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
    