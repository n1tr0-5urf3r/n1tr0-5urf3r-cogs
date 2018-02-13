import discord
from discord.ext import commands
import time
from .utils import checks
from cogs import * #dataIO, fileIO
from __main__ import send_cmd_help

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
    async def pizza(self,ctx):
        """Pizza!"""
        await self.bot.say('David muss sich noch überlegen, was hier passieren soll.')

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
        """Create custom emojis Currently not working"""
        server = ctx.message.server
        with open('/opt/Red-DiscordBot/cogs/icon.png', 'rb') as imageFile:
            f = imageFile.read()
        await self.bot.create_custom_emoji(server=server, name='temp', image=f)

    @commands.command(pass_context=True)
    async def just(self, ctx):
        """Displays general help information for my guild"""
        user = ctx.message.author
        color = self.getColor(user)

        data = discord.Embed(description='Erklärung zu den Befehlen', color=color)
        data.set_author(name='Justified Loyalty')
        data.add_field(name='Schlüssel hinzufügen', value='*!key add <schlüssel>*  Fügt euren Schlüssel hinzu, wird benötigt, um Daten auszulesen.', inline=False)
        data.add_field(name='Informationen zur Gilde', value='*!guild info Justified Loyalty* (nur für Gildenleader)', inline=False)
        data.add_field(name='Gildenmitglieder anzeigen', value='*!guild members Justified Loyalty* (nur für Gildenleader)', inline=False)
        data.add_field(name='Inhalt der Schatzkammer anzeigen', value='*!guild treasury Justified Loyalty* (nur für Gildenleader)', inline=False)
        data.add_field(name='Informationen zum Charakter', value='*!character info <name>*', inline=False)
        data.add_field(name='Informationen zum Account', value='*!account*', inline=False)
        data.add_field(name='PvP Statistiken', value='*!pvp stats*', inline=False)
        data.add_field(name='Auktionen im Handelsposten einsehen', value='*!tp current buys/sells*', inline=False)
        data.add_field(name='Lieferungen im Handelsposten einsehen', value='*!tp delivery*', inline=False)
        data.add_field(name='WvW Punktestand', value='*!wvw info*  Kann auch mit anderen Servern aufgerufen werden.', inline=False)
        data.add_field(name='Geldbeutelinhalt (Geld oder Dungeonmarken) anzeigen', value='*!wallet show/tokens*', inline=False)
        data.add_field(name='Dailies anzeigen', value='*!daily pvp/pve/wvw/fractals*', inline=False)
        data.set_footer(text='Bei Fragen an Fabi wenden')
        data.set_thumbnail(url='https://cdn.discordapp.com/emojis/294742647069868032.png')

        await self.bot.say(embed=data)

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
            try:
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

            except socket.gaierror:
                await self.bot.say('Whoops! That Address cant be resolved!')

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
            line = file.readlines()[50]
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

    @commands.command(pass_context=True)
    async def coinflip(self, *,player1=None, player2=None):
        """Coinflip, defaults to Kopf/Zahl if no players are given"""
        rng = randint(1,10)
        if rng < 5:
            return await self.bot.say("{} hat gewonnen!".format(player1))
        else:
            return await self.bot.say("{} hat gewonnen!".format(player2))


    def getColor(self, user):
        try:
            color = user.colour
        except:
            color = discord.Embed.Empty
        return color


def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
