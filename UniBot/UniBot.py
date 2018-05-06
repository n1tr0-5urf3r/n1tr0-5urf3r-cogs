# Discord stuff
import discord
import asyncio
import aiohttp
from discord.ext import commands
import re
import datetime
import requests


class UniBot:
    """ Command definitions"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)

    def __unload(self):
        self.session.close()

        @commands.command(pass_context=True)
        async def mensa(self, ctx, subcommand=None):
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

            # Grant permissions to role
            for channel in all_channels:
                if "übungsgruppe-" in channel.name:
                    role = discord.utils.get(server.roles, name=channel.name)
                    # Deny permission to everyone
                    await self.bot.edit_channel_permissions(channel, server.default_role, everyone_perms)
                    # Grant permission to role
                    await self.bot.edit_channel_permissions(channel, role, overwrite)
                    await self.bot.say("Granted permissions for role {} to channel {}".format(role, channel))
                    await asyncio.sleep(1.5)

        @commands.command(pass_context=True)
        async def gruppe(self, ctx, join_group=None):
            server = ctx.message.server

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

                await self.bot.say("Gruppe nicht gefunden oder angegeben. Verfügbare Gruppen sind:")
                embed.set_footer(text='Bot by Fabi')
                return await self.bot.say(embed=embed)

            if join_group is None:
                return await send_help()
            join_group = join_group.lower()
            join_group = "übungsgruppe-{}".format(join_group)
            author = ctx.message.author
            if "übungsgruppe-" in join_group:
                try:
                    role = discord.utils.get(server.roles, name=join_group)
                    await self.bot.add_roles(author, role)
                    await self.bot.say("{}, du wurdest zu {} hinzugefügt".format(author.mention, join_group))
                except AttributeError:
                    await send_help()
            else:
                await send_help()

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
                    await send_help()
                else:
                    await self.bot.remove_roles(author, role)
                    await self.bot.say(
                        "{} du wurdest aus der Gruppe {} entfernt".format(author.mention, leave_group_full))
            except AttributeError:
                await send_help()

def setup(bot):
    n = UniBot(bot)
    loop = asyncio.get_event_loop()
    bot.add_cog(n)
    