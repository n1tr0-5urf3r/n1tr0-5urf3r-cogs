import discord
from discord.ext import commands
import time
#from .utils import checks
from cogs import * #dataIO, fileIO
#from __main__ import send_cmd_help

# Used for DNS lookup
import socket
# Used for regexp
import re
# Used for ping
import os
import urllib.request
import requests
from random import randint
# General stuff for discord
import asyncio
import aiohttp
import datetime

client = discord.Client()

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
        game = discord.Game(name='Justified Loyalty')
        await self.bot.change_status(game)

    @commands.command(pass_context=True)
    async def beleidige(self, ctx, name):
        """Second Test, Variablenverarbeitung"""
        msg = await self.bot.say(name + ' ist ein Behindi!')
        await self.bot.add_reaction(msg,'😲')

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await self.bot.say('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await self.bot.say(embed=data)

    @commands.command(pass_context=True)
    async def create(self, ctx):
        """Create custom emojis"""
        server = ctx.message.server
        with open('/opt/Red-DiscordBot/cogs/icon.png', 'rb') as imageFile:
            f = imageFile.read()
        await self.bot.create_custom_emoji(self,server, 'temp', f)

    @commands.command(pass_context=True)
    async def ping(self, ctx, ip):
        """Check if Server is online"""

        # Check for valid IP else do DNS lookup
        valid_ip = re.compile("[0-9]{,3}\.[0-9]{,3}\.[0-9]{,3}")
        valid_hostname = re.compile(".*\.[a-zA-Z]{2,}")
        valid = False

        if valid_ip.match(ip):
            valid = True
        elif valid_hostname.match(ip):
            valid = True
            await self.bot.say('Doing DNS lookup...')
            ip = socket.gethostbyname(ip)
        if valid == True:
            start = time.time()
            response = os.system("sudo ping -c 1 -w3 " + ip)
            duration = time.time() - start
            duration = round(duration * 1000, 0)
            if response == 0:
                await self.bot.say(ip + ' is up and responding in ' + str(duration) + 'ms.')
            else:
                await self.bot.say(ip + ' is not reachable.')
        else:
            await self.bot.say(ip + ' is not a valid IP or Domain.')

    @commands.command(pass_context=True)
    async def pr0(self,ctx):
        """Outputs a random image from pr0gramm.com (sfw)"""

        # Generate random number, check if header responds with 200 (OK)
        # If not generate new number
        # Hardcoded img src from webpage in line 63
        # Extract path to image from webpage
        # Clean up
        match = False
        while not match:
            # RNG
            valid = False
            while not valid:
                post = str(randint(0, 1831010))
                ret = requests.head('http://pr0gramm.com/static/'+post)
                #await self.bot.say('DEBUG Statuscode: ' + str(ret.status_code))
                if ret.status_code != 404:
                    valid = True
                    # Download page from static pr0gramm, save to tempfile
                    urllib.request.urlretrieve('http://pr0gramm.com/static/' + post, 'temp.html')
                #elif ret.status_code == 404:
                #    await self.bot.say('DEBUG 404:' + post + ' Statuscode: ' + str(ret.status_code))

            file = open('temp.html', 'r')
            line = file.readlines()[62]
            if "img src" in line:
                tags = re.sub('^.*alt="', '', line)
                tags = tags.replace('"/>', '')
                line = line.replace('<img src="','http:')
                line = re.sub('".*$', '', line)
                await self.bot.say('Tags: ' + tags)
                await self.bot.say(line)
                match = True
                file.close()
                os.remove('temp.html')


def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)