import discord
from discord.ext import commands
import time

# Used for DNS lookup
import socket
# Used for regexp
import re
# Used for ping
import os
from random import randint
import random
# General stuff for discord
import asyncio
import aiohttp
import urllib.request, json

# Discord stuff
import datetime
import requests

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

    # @commands.command(pass_context=True)
    # async def beleidige(self, ctx, name):
    #     """Second Test, Variablenverarbeitung"""
    #     msg = await self.bot.say(name + ' ist ein Behindi!')
    #     await self.bot.add_reaction(msg, '😲')

    @commands.command(pass_context=True)
    async def pizza(self, ctx):
        """Pizza!"""
        pizza_list = [
            'https://media1.giphy.com/media/iThaM3NlpjH0Y/200w.gif',
            'https://media1.giphy.com/media/POmeDOmoTg9CU/200w.gif',
            'https://i.imgur.com/BrXB1VU.gifv',
            'https://media0.giphy.com/media/3o7aDdeZzsZyx4qkqk/200w.gif',
            'https://media0.giphy.com/media/sTUWqCKtxd01W/200w.gif',
            'https://media0.giphy.com/media/YfLdTsfMIfHX2/200w.gif',
            'https://media0.giphy.com/media/AeWntMyxGFXXi/200w.gif',
            'https://media0.giphy.com/media/10kxE34bJPaUO4/giphy.gif',
            'https://media0.giphy.com/media/RRRSdQ6tuUXBu/200w.gif'
        ]

        rng = random.randint(0, len(pizza_list))
        await self.bot.say(pizza_list[rng])

    @commands.command(pass_context=True)
    async def emojis(self, ctx):
        """Returns a list of all Server Emojis"""
        server = ctx.message.server
        await self.bot.say('This may take some time, generating list...')
        data = discord.Embed(description="Emojilist")
        for ej in server.emojis:
            data.add_field(
                name=ej.name, value=str(ej) + " " + ej.id, inline=False)
        await self.bot.say(embed=data)

    # @commands.command(pass_context=True)
    # async def create(self, ctx):
    #     """Create custom emojis Currently not working"""
    #     server = ctx.message.server
    #     with open('/opt/Red-DiscordBot/cogs/icon.png', 'rb') as imageFile:
    #         f = imageFile.read()
    #     await self.bot.create_custom_emoji(server=server, name='temp', image=f)

    @commands.command(pass_context=True)
    async def just(self, ctx):
        """Displays general help information for my guild"""
        user = ctx.message.author
        color = self.getColor(user)

        data = discord.Embed(
            description='Erklärung zu den Befehlen', color=color)
        data.set_author(name='Justified Loyalty')
        data.add_field(
            name='Schlüssel hinzufügen',
            value=
            '*!key add <schlüssel>*  Fügt euren Schlüssel hinzu, wird benötigt, um Daten auszulesen.',
            inline=False)
        data.add_field(
            name='Informationen zur Gilde',
            value='*!guild info Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Gildenmitglieder anzeigen',
            value='*!guild members Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Inhalt der Schatzkammer anzeigen',
            value='*!guild treasury Justified Loyalty* (nur für Gildenleader)',
            inline=False)
        data.add_field(
            name='Informationen zum Charakter',
            value='*!character info <name>*',
            inline=False)
        data.add_field(
            name='Informationen zum Account', value='*!account*', inline=False)
        data.add_field(
            name='PvP Statistiken', value='*!pvp stats*', inline=False)
        data.add_field(
            name='Auktionen im Handelsposten einsehen',
            value='*!tp current buys/sells*',
            inline=False)
        data.add_field(
            name='Lieferungen im Handelsposten einsehen',
            value='*!tp delivery*',
            inline=False)
        data.add_field(
            name='WvW Punktestand',
            value=
            '*!wvw info*  Kann auch mit anderen Servern aufgerufen werden.',
            inline=False)
        data.add_field(
            name='Geldbeutelinhalt (Geld oder Dungeonmarken) anzeigen',
            value='*!wallet show/tokens*',
            inline=False)
        data.add_field(
            name='Dailies anzeigen',
            value='*!daily pvp/pve/wvw/fractals*',
            inline=False)
        data.set_footer(text='Bei Fragen an Fabi wenden')
        data.set_thumbnail(
            url='https://cdn.discordapp.com/emojis/294742647069868032.png')

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
                        await self.bot.say(ip + ' is up and responding in ' +
                                           str(duration) + 'ms.')
                    else:
                        await self.bot.say(ip + ' is not reachable.')
                else:
                    await self.bot.say(ip + ' is not a valid IP or Domain.')

            except socket.gaierror:
                await self.bot.say('Whoops! That Address cant be resolved!')

    @commands.command(pass_context=True)
    async def pr0(self, ctx):
        """Outputs a random image from pr0gramm.com (sfw)"""

        # Generate random number, check if header responds with 200 (OK)
        # If not generate new number
        # Hardcoded img src from webpage in line 63
        # Extract path to image from webpage
        # Clean up
        user = ctx.message.author
        color = self.getColor(user)

        with urllib.request.urlopen(
                "https://pr0gramm.com/api/items/get") as url:
            data = json.loads(url.read().decode())

        items = data["items"]
        item = random.choice(items)["image"]
        upvotes = random.choice(items)["up"]
        downvotes = random.choice(items)["down"]
        uploader = random.choice(items)["user"]
        embed = discord.Embed(
            description='Uploaded by **{}**'.format(uploader), color=color)
        embed.add_field(
            name="Score",
            value="{0} :arrow_up: {1} :arrow_down:".format(upvotes, downvotes))

        await self.bot.say(embed=embed)
        await self.bot.say("https://img.pr0gramm.com/{}".format(item))

    @commands.command(pass_context=True)
    async def coinflip(self, ctx, player1=None, *, player2=None):
        """Coinflip, defaults to Kopf/Zahl if no players are given"""
        rng = randint(1, 10)

        if player1 is None and player2 is None:
            if rng < 5:
                return await self.bot.say("Kopf gewinnt!")
            else:
                return await self.bot.say("Zahl gewinnt!")
        else:
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

    @commands.command(pass_context=True)
    async def mensa(self, ctx, subcommand=None):
        return await self.bot.say("Der Speiseplan wird vom Studierendenwerk leider zurzeit nicht mehr zur Verfügung gestellt.")
        user = ctx.message.author
        color = self.getColor(user)

        # Get current calendarweek
        today = datetime.datetime.now()
        cal_week = today.strftime("%W")

        # Probably should make this in a subcommand
        weekday = datetime.datetime.today().weekday()
        week_start = today - datetime.timedelta(days=weekday)
        week_end = today + datetime.timedelta(days=4 - weekday)
        if subcommand:
            if subcommand.lower() == "nextweek" or subcommand.lower() == "nw":
                cal_week = int(cal_week) + 1
                weekday = 0
                week_start = today + datetime.timedelta(days=(7 - today.weekday()))
                week_end = week_start + datetime.timedelta(days=4)
            elif subcommand.lower() == "help" or subcommand.lower() == "h":
                return await self.bot.say("""```
Mensa:
    help         Diese Nachricht
    <leer>       Speiseplan der aktuellen Woche
    nextweek     Speiseplan der nächsten Woche
                                
    z.B. !mensa oder !mensa nextweek
    Alternativ auch Abkürzungen wie "h" oder "nw"
```""")
        # Show next week on weekends
        if weekday > 4:
            cal_week = int(cal_week) + 1
            weekday = 0
            week_start = today + datetime.timedelta(days=(7 - today.weekday()))
            week_end = week_start + datetime.timedelta(days=4)

        url_mensa = "https://www.my-stuwe.de/mensa/mensa-morgenstelle-tuebingen/?woche={}".format(cal_week)

        r = requests.get(url_mensa)
        html_mensa = re.sub('\n', ' ', r.content.decode('utf8'))
        tagesmenu = re.findall(r"(<td>Tagesmenü</td>.*?)(</td>)", html_mensa)
        tagesmenu_veg = re.findall(r"(<td>Tagesmenü vegetarisch</td>.*?)(</td>)", html_mensa)
        mensa_vital = re.findall(r"(<td>mensaVital.*?</td>.*?)(</td>)", html_mensa)
        tages_angebot = re.findall(r"(<td>Angebot des Tages</td>.*?)(</td>)", html_mensa)

        def cleanUp(menu):
            daily_menu = []
            for m in menu:
                t_menu = re.sub("(<.*?>)", "", m[0])
                t_menu = re.sub("  |, ", "\n- ", t_menu)
                t_menu = re.sub("Tagessuppe ", "Tagessuppe\n- ", t_menu)
                t_menu = re.sub(
                    "Tagesmenü vegetarisch|Tagesmenü|mensaVital vegan|mensaVital vegetarisch|mensaVital|Angebot des Tages",
                    "", t_menu)
                daily_menu.append((t_menu))
            return daily_menu

        menu1 = cleanUp(tagesmenu)
        menu2 = cleanUp(tagesmenu_veg)
        menu3 = cleanUp(mensa_vital)
        menu4 = cleanUp(tages_angebot)

        embed = discord.Embed(
            description="Mensa Morgenstelle, KW {} vom {} bis {}".format(cal_week, week_start.strftime("%d.%m."),
                                                                         week_end.strftime("%d.%m.")), color=color)

        if weekday > 0:
            counter = 0 + weekday
        else:
            counter = 0
        wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        for speise in menu1:
            try:
                vegetarisch = menu2[counter - weekday]
            except IndexError:
                vegetarisch = ""
            try:
                vegan = menu3[counter - weekday]
            except IndexError:
                vegan = ""
            try:
                angebot = menu4[counter - weekday]
            except IndexError:
                angebot = ""
            embed.add_field(name="{}".format(wochentage[counter]),
                            value="*Tagesmenü:*\n- {}\n\n*Tagesmenü vegetarisch:*\n- {}\n\n*MensaVital:*\n- {}\n\n*Angebot des Tages:*\n- {}\n".format(
                                speise, vegetarisch, vegan, angebot), inline=False)
            counter += 1

        embed.set_thumbnail(
            url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg/220px-Studentenwerk_T%C3%BCbingen-Hohenheim_logo.svg.png')
        embed.set_footer(text='Bot by Fabi')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_role("Administrator")
    async def createroles(self, ctx):
        """Create roles to each channel that begins with "übungsgruppe- and set permissions"""
        server = ctx.message.server
        author = ctx.message.author
        all_channels = server.channels
        all_roles = []
        group_channels = []
        # Collect already available roles
        for role in server.roles:
            all_roles.append(role.name)
        # Collect needed channel names
        for channel in all_channels:
            if "übungsgruppe-" in channel.name:
                if channel.name not in group_channels:
                    group_channels.append(channel.name)

        # Needed permissions
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        overwrite = discord.PermissionOverwrite()
        overwrite.read_messages = True
        overwrite.send_message = True
        overwrite.manage_messages = True
        overwrite.embed_links = True
        overwrite.attach_files = True
        overwrite.read_message_history = True
        # Create a role for each channel
        for group_channel in group_channels:
            if group_channel not in all_roles:
                await self.bot.create_role(author.server, name=group_channel)
                await self.bot.say("Role {} created".format(group_channel))

        role_bots = discord.utils.get(server.roles, name="Bots")

        # Grant permissions to role
        for channel in all_channels:
            if "übungsgruppe-" in channel.name:
                role = discord.utils.get(server.roles, name=channel.name)
                # Deny permission to everyone
                await self.bot.edit_channel_permissions(channel, server.default_role, everyone_perms)
                # Grant permission to role
                await self.bot.edit_channel_permissions(channel, role, overwrite)
                await self.bot.edit_channel_permissions(channel, role_bots, overwrite)
                await self.bot.say("Granted permissions for role {} to channel {}".format(role, channel))
                await asyncio.sleep(1.5)

    @commands.command(pass_context=True)
    async def gruppe(self, ctx, join_group=None):

        server = ctx.message.server


        async def send_help(destination):
            group_channels = []
            all_channels = server.channels
            for channel in all_channels:
                if "übungsgruppe-" in channel.name:
                    if channel.name not in group_channels:
                        group_channels.append(channel.name.replace("übungsgruppe-", ""))
            sorted_groups = sorted(group_channels)
            embed = discord.Embed(
                description="**Verfügbare Übungsgruppen**")
            embed.add_field(name="Gruppen", value="\n".join(sorted_groups))

            await self.bot.send_message(destination, "Gruppe nicht gefunden oder angegeben. Verfügbare Gruppen sind:")
            embed.set_footer(text='Bot by Fabi')
            return await self.bot.send_message(destination, embed=embed)

        # Harcoded channel ID :(
        if ctx.message.channel.id is not "438732571166375938":
            await self.bot.say("Falscher channel " + ctx.message.channel.id)
            await send_help(ctx.message.author)
            await self.bot.send_message(ctx.message.author, "Bitte nutze den Channel #gruppenzuweisung dazu!")

        else:
            if join_group is None:
                return await send_help(ctx.message.channel)
            join_group = join_group.lower()
            join_group = "übungsgruppe-{}".format(join_group)
            author = ctx.message.author
            if "übungsgruppe-" in join_group:
                try:
                    role = discord.utils.get(server.roles, name=join_group)
                    await self.bot.add_roles(author, role)
                    await self.bot.say("{}, du wurdest zu {} hinzugefügt".format(author.mention, join_group))
                except AttributeError:
                    await send_help(ctx.message.channel)
            else:
                await send_help(ctx.message.channel)

    @commands.command(pass_context=True)
    async def gruppeverlassen(self, ctx, leave_group=None):
        server = ctx.message.server
        author = ctx.message.author
        all_roles = author.roles
        role_names = []
        for role_name in all_roles:
            if not "everyone" in role_name.name:
                role_names.append(role_name.name.replace("übungsgruppe-", ""))

        async def send_help():
            embed = discord.Embed(description="**Zugeordnete Übungsgruppen**")
            embed.add_field(name="Gruppen", value="\n".join(role_names))
            await self.bot.say("Gruppe nicht gefunden oder zugeordnet. Zugeordnete Gruppen sind:")
            embed.set_footer(text='Bot by Fabi')
            return await self.bot.say(embed=embed)

        if leave_group is None:
            return await send_help()
        leave_group = leave_group.lower()
        leave_group_full = "übungsgruppe-{}".format(leave_group)
        try:
            role = discord.utils.get(server.roles, name=leave_group_full)
            if leave_group not in role_names:
                await self.bot.say("{} du bist nicht in der Gruppe {}".format(author.mention, leave_group_full))
            else:
                await self.bot.remove_roles(author, role)
                await self.bot.say("{} du wurdest aus der Gruppe {} entfernt".format(author.mention, leave_group_full))
        except AttributeError:
            await send_help()

    @commands.command(pass_context=True)
    async def gruppeninfo(self, ctx, group=None):
        server = ctx.message.server
        color = self.getColor(ctx.message.author)
        channel = ctx.message.channel
        group_info = None

        # redundant part, fix this
        async def send_help():
            group_channels = []
            all_channels = server.channels
            for channel in all_channels:
                if "übungsgruppe-" in channel.name:
                    if channel.name not in group_channels:
                        group_channels.append(channel.name.replace("übungsgruppe-", ""))
            sorted_groups = sorted(group_channels)
            embed = discord.Embed(
                description="**Verfügbare Übungsgruppen**")
            embed.add_field(name="Gruppen", value="\n".join(sorted_groups))

            return await self.bot.say(embed=embed)

        if group is not None:
            group_info = "übungsgruppe-{}".format(group)

        if "übungsgruppe-" in channel.name and group is None:
            group_info = channel.name
        elif group is None:
            return await send_help()
        group_info = group_info.lower()
        role = discord.utils.get(server.roles, name=group_info)

        member_list = []
        members = server.members
        for member in members:
            # Check if member has role
            roles_member = member.roles
            if role in roles_member:
                if member.nick:
                    member_list.append(member.nick)
                else:
                    member_list.append(member.name)
        embed = discord.Embed(description="**Zugeordnete Mitglieder**", color=color)
        if member_list:
            embed.add_field(name=group_info, value="\n".join(member_list))
        else:
            embed.add_field(name=group_info, value="Niemand")
        return await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def faq(self, ctx):
        embed = discord.Embed(description="FAQ", color=0xff0000)
        embed.add_field(name="Q: Was hat es mit der Gewitterwolke im InfoMark auf sich?\n ", value="""\n**A:** Die Wolke zeigt an dass der Code-Test auf InfoMark fehlgeschlagen ist, da aber 
   keine Tests mehr gemacht werden zeigt die Wolke immer einen Fehler an.\n""")
        embed.add_field(name="Q: Wie kann ich mich in die Tutorien-Gruppe eintragen?", value="""**A:** Der Befehl "!gruppe" zeigt die Übungsgruppen an, die zur Verfügung stehen. Mit
   "gruppe [NAME DER GRUPPE]" trägt man sich in diese ein. Mit "gruppeverlassen [NAME DER GRUPPE]
   kann man sich aus einer Gruppe austragen. Dafür steht der Channel #gruppenzuweisung bereit.
   Ein Beispiel: !gruppe m2-mo-12-14 , !gruppeverlassen m2-mo-12-14\n""")
        embed.add_field(name="Q: Wie kann ich beim Music-Bot ein Lied in die Warteschlange setzen?",
                        value="**A:** Der Befehl dafür ist: \"$play [LINK DES LIEDS]\" oder \"$play [NAME DES LIEDS]\", dabei sucht es automatisch.\n")
        embed.add_field(name="Q: Sollen beide Gruppenpartner die Lösung für das aktuelle Lösungsblatt abgeben?",
                        value="**A:** Solange beide Namen auf dem Blatt stehen reicht es wenn einer abgibt.\n")
        embed.add_field(name="Q: Wie füge ich die .java Vorlage aus InfoMark in Eclipse ein?", value="""**A:** Zuerst muss man ein neues Projekt anlegen (oder ein schon vorhandenes benutzen), 
   dann muss man ein Package erstellen das den gleichen Namen hat, wie in der Vorlage definiert.
   Ein Beispiel: in Eclipse heißt es "package HW1;", dann muss auch das eigene Package "HW1" heißen.\n""")
        embed.add_field(name="Q: Wie kann ich noch einen Übungspartner finden? ", value="""**A:** Es gibt viele Möglichkeiten noch einen Übungspartner zu finden. Beispielsweise in der #tauschbörse oder 
   in den Gruppen des jeweiligen Tutoriums.\n""")
        embed.add_field(name="Q: Müssen wir in Partnerarbeit abgeben?", value="""**A:** Bestenfalls ja. Je weniger die Tutoren zu korrigieren haben, desto mehr Zeit können sie sich pro Korrektur 
   nehmen, was unter Umständen auch zu mehr Punkten führt. In Ausnahmefällen ist es aber trotzdem möglich, das 
   aber erst mit dem jeweiligen Tutor abklären.\n""")
        embed.add_field(name="Q: Kann mein Übungspartner in einer anderen Übungsgruppe sein?", value="""**A:** Solange ihr den gleichen Tutor habt sollte das kein Problem sein. Sind es unterschiedliche Tutoren, dann
   eher ungern, aber in Ausnahmefällen dennoch möglich. So oder so bitte dennoch mit dem jeweiligen Tutor(en) 
   abklären.\n""")
        embed.add_field(name="Q: Wo findet der HelpDesk statt?", value="""**A:** Für Informatik: C-Bau, Raum N03; C-Bau, Raum H13; C-Bau, Raum H33.
   Für Mathe: B-Bau, Raum B9N22.\n""")
        embed.add_field(name="Q: Gibt es ein Skript?", value="""**A:** Für Informatik: Es gibt kein Skript, aber die Folien aus der Vorlesung sind im InfoMark.
   Für Mathe: Hier gibt es auch kein Skript, Vic ist aber so nett und erstellt selbstständig mit LaTeX eines.
   Für Logik: Auch hier gibt es kein Skript, die Folien sind aber in der Ilias.\n""")
        embed.add_field(name="Q: Wie gebe ich die Lösungen für das Übungsblatt ab?", value="""**A:** Für Informatik: Sie wird online im InfoMark abgegeben.
   Für Mathe: Es werden Ordner in der Vorlesung ausgelegt, mit den Namen der Tutoren darauf.
   Für IdS: Sie werden online im Moodle abgegeben.
   Für GDI: Wie in IdS.\n""")

        return await self.bot.say(embed=embed)


def setup(bot):
    n = Ihlebot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
