#! /usr/bin/env python3
"""
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from colorama import init

print("[Loaded colorama::init]")
from colorama import Fore as F

print("[Loaded colorama::Fore]")
from colorama import Style as S

print("[Loaded colorama::Style]")
from colorama import Back as B

print("[Loaded colorama::Back]")
init()
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Initialized colorama]")
import asyncio

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded asyncio]")
import discord

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded discord]")
from discord.ext import commands

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded discord::commands]")
from discord.ext.commands import CommandNotFound

print(
    S.BRIGHT
    + F.GREEN
    + "[OK]\t"
    + S.RESET_ALL
    + "[Loaded discord::commands::CommandNotFound]"
)
from discord.voice_client import VoiceClient

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded discord::VoiceClient]")
from datetime import datetime

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded datetime::datetime]")
import random

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded random]")
import logging

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded logging]")

from cn_globals import (
    RIGGED,
    DB,
    AUTHOR,
    VERSION,
    SILENT,
    RANDOM_EVENT_AMOUNT,
    RANDOM_EVENT_CURRENTLY,
    CRATE_GIVES_XP,
    CRATE_REWARD_AMOUNT,
    CRATE_SPAWNED,
    FILTER_BOTS,
    FILTER_LOGS,
    FILTER_USERS,
    DB_PUSH_TIMEOUT,
    FINE_AMOUNT,
    BRIBE_PRICE,
    LOTTO_REWARD,
    DAILY_BONUS,
    TOKEN,
    MATERIALS_PER_ITEM,
)

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded cn_globals]")
import cndb

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded cndb]")
from RPG import Generator

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded RPG::Generator]")
from collections import namedtuple

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded collections::namedtuple]")
import os

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded os]")
import sys

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded sys]")
from typing import Dict, List

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded typing::Dict]")
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded typing::List]")
from subprocess import Popen

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded subprocess::Popen]")
import json

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded json]")
from game import Game, GAME_OPTIONS, GameState

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded game::Game]")
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded game::GAME_OPTIONS]")
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded game::GameState]")
import pot

print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Loaded pot]")

DATABASE = cndb.CNDatabase()
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Initialized Database]")
GENERATOR = Generator()
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Initialized Generator]")
GAME: Game = Game()
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Initialized Game]")
DATABASE.pull()

RAID_PLAYERS = []
RAID_BOSS = {}


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
print(
    S.BRIGHT
    + F.GREEN
    + "[OK]\t"
    + S.RESET_ALL
    + "[Set logging to INFO|WARNING|ERROR|CRITICAL]"
)

# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix="?", case_insensitive=True)
print(S.BRIGHT + F.GREEN + "[OK]\t" + S.RESET_ALL + "[Initialized Bot]")

# Helper function. Sends a debug message to the console. Used to standardize input and make changes easier, and debugs clearer.
def debug_console_log(source: str, author: discord.User, msg: str = "") -> None:
    global RIGGED
    global FILTER_LOGS

    is_admin: bool = author.top_role.permissions.administrator
    if not FILTER_LOGS:
        print(
            S.BRIGHT
            + F.YELLOW
            + "[DEBUG|LOG]\t#{}: ({}) {}: {}\n[DEBUG|LOG]\tRigged: {} - Admin: {}".format(
                source, author.id, author.name, msg, RIGGED, is_admin
            )
        )


def compose_embed(color, name: str, content: str) -> discord.Embed:
    msg = discord.Embed(title="CN Bot", description="", color=color)
    msg.add_field(name=name, value=content, inline=False)
    return msg


# Bot events
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    print(F.RED + S.BRIGHT)
    raise error


async def push_database_task():
    global DATABASE
    # global RPGCTRL
    global DB_PUSH_TIMEOUT

    while True:
        DATABASE.push()
        # RPGCTRL.push()
        await asyncio.sleep(DB_PUSH_TIMEOUT)


@bot.event
async def on_ready():
    global AUTHOR
    global VERSION

    bot.loop.create_task(push_database_task())
    # Forge a header with bot info
    now = datetime.now()
    server_count: int = len(bot.guilds)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="{} servers | ?help".format(server_count),
        )
    )
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    if not hasattr(bot, "appinfo"):
        bot.appinfo = await bot.application_info()
    print(
        S.BRIGHT
        + B.WHITE
        + F.BLUE
        + "--------------------------------------------------------------------------------"
    )
    print("Bot connected\t\t{} [V:{}]\t\t\t\t".format(date_time, VERSION))
    print(
        "ID:\t\t\t{}\t\t\t\t\t\nName:\t\t\t{}\t\t\t\t\t\nOwner:\t\t\t{}\t\t\t\t\t\t\nAuthor:\t\t\t{}\t\t\t\t".format(
            bot.appinfo.id, bot.appinfo.name, bot.appinfo.owner, AUTHOR
        )
    )
    print(
        "--------------------------------------------------------------------------------"
        + S.RESET_ALL
    )


@bot.event
async def on_message(message):
    # Necessary globals to do on_message events
    global RANDOM_EVENT_CURRENTLY
    global RANDOM_EVENT_AMOUNT
    global FILTER_LOGS
    global FILTER_BOTS
    global FILTER_USERS
    global CRATE_SPAWNED
    global CRATE_GIVES_XP
    global CRATE_REWARD_AMOUNT
    global DATABASE
    global SILENT
    # Necessary variables for logging, events, etc.
    # Also cleaning of message contents for a better reading experience
    rnd = random.randint(0, 5000)
    author = message.author
    content = message.content
    content = content.replace("*", "")
    content = content.replace("`", "")
    content = content.replace("_", "")
    content = content.replace("~", "")
    # We dont want to give bots xp
    if not author.bot:
        msg = DATABASE.register(author)
        if msg != None:
            print("User {} has been registered!".format(author.name))
        xp = random.randint(10, 25)
        debug_console_log("on_message", author, "awarded {}xp for messsage".format(xp))
        xp_return: int = DATABASE.update_db(
            author.id, xp, False, False, True
        )  # -1 if not registered
        if xp_return == -1:
            print("User {} has been registered!".format(author.name))
    # Random cash events
    if rnd < 100 and rnd > 10 and not RANDOM_EVENT_CURRENTLY and not SILENT:
        RANDOM_EVENT_CURRENTLY = True
        RANDOM_EVENT_AMOUNT = random.randint(100, 10000)
        print(
            S.BRIGHT
            + F.YELLOW
            + "[DEBUG|LOG]\tRandom event for ¤{} created".format(RANDOM_EVENT_AMOUNT)
        )
        await message.channel.send(
            "¤{} just materialized out of nothing, get it with `?grab`!".format(
                RANDOM_EVENT_AMOUNT
            )
        )
    # Random crate event
    elif rnd < 10 and not RANDOM_EVENT_CURRENTLY and not SILENT:
        RANDOM_EVENT_CURRENTLY = True
        coinflip: int = random.randint(0, 100)
        if coinflip < 50:
            CRATE_GIVES_XP = True
        crate_rarity_roll: int = random.randint(0, 100)
        crate_rarity: str = "Trash"
        if crate_rarity_roll < 75:
            crate_rarity = "Common"
        if crate_rarity_roll < 50:
            crate_rarity = "Uncommon"
        if crate_rarity_roll < 25:
            crate_rarity = "Rare"
        if crate_rarity_roll < 10:
            crate_rarity = "Epic"
        CRATE_REWARD_AMOUNT = (100 - crate_rarity_roll) * 100
        if not CRATE_GIVES_XP:
            CRATE_REWARD_AMOUNT *= 100
        CRATE_SPAWNED = True
        print(
            S.BRIGHT
            + F.YELLOW
            + "[DEBUG|LOG]\tRandom crate for ¤{} created (Gives XP instead of Money: {})".format(
                CRATE_REWARD_AMOUNT, CRATE_GIVES_XP
            )
        )
        await message.channel.send(
            "***A(n) {} crate was just created! Unbox it with*** `?unbox`***!***".format(
                crate_rarity
            )
        )

    # Logging
    if not author.bot and not FILTER_USERS:
        print(
            S.BRIGHT
            + F.CYAN
            + "[@/USER]\t({}) {}: {}".format(author.id, author.name, content)
        )
    if author.bot and not FILTER_BOTS:
        print(S.BRIGHT + F.MAGENTA + "[@/BOT]\t{}: {}".format(author.name, content))
    # Make sure commands work
    await bot.process_commands(message)


@bot.event
async def on_disconnect():
    global DATABASE

    DATABASE.push()
    print(B.WHITE + F.RED + "Lost connection! Wrote internal state." + S.RESET_ALL)


bot.remove_command("help")
# Help messages
@bot.command(aliases=["h", "info", "commands", "c"])
async def help(ctx):
    """
	help: 	
			displays a help message
	Requires:
			Nothing
	"""
    debug_console_log("help", ctx.message.author)
    if ctx.message.author.dm_channel == None:
        await ctx.message.author.create_dm()
        channel = ctx.message.author.dm_channel
        print(channel)
    helpmsg = discord.Embed(title="CN Bot", description="", color=0xFF00FF)
    helpmsg.add_field(
        name="?help",
        value="Displays this message.\nAlias=[h, info, commands, c]",
        inline=False,
    )
    helpmsg.add_field(
        name="?roll <dice><sides>[mod]",
        value="Rolls some variable-sided dice and prints the result.\nAlias=[r]",
        inline=False,
    )
    helpmsg.add_field(name="?rigg", value="Nice try", inline=False)
    helpmsg.add_field(name="?rigged", value="How dare you!", inline=False)
    helpmsg.add_field(
        name="?gamble <bet>",
        value="Dicegame, betting ¤<bet> against a 100-sided roll, over 55 is a win.\nAlias=[55x2, g, bet]",
        inline=False,
    )
    helpmsg.add_field(
        name="?steal <target>",
        value="3% chance to steal 10-20% of the targets money.\nAlias=[s, rob, thieve]",
        inline=False,
    )
    helpmsg.add_field(
        name="?bribe",
        value="Pay the court a bribe to remove your reputation and reset the theft counter",
        inline=False,
    )
    helpmsg.add_field(
        name="?slots <amount>", value="Bet an amount on a slot machine!", inline=False
    )
    helpmsg.add_field(
        name="?lottery",
        value="Play the lottery! Insanely low chance at a lot of money!\nAlias=[lotto, l]",
        inline=False,
    )
    helpmsg.add_field(
        name="?bal",
        value="Shows you how much money you have.\nAlias=[balance, eco, money]",
        inline=False,
    )
    helpmsg.add_field(
        name="?daily", value="Claim a daily cash bonus.\nAlias=[d]", inline=False
    )
    helpmsg.add_field(
        name="?order <drink>",
        value="Buy a drink! userexperiencenotguaranteed",
        inline=False,
    )
    helpmsg.add_field(
        name="?cookie <user>", value="Give someone a cookie!", inline=False
    )
    helpmsg.add_field(
        name="?pay <user> <amount>",
        value="Send someone your hard-earned money.\nAlias=[give]",
        inline=False,
    )
    helpmsg.add_field(
        name="?insult <name>", value="Generate an insult aimed at someone", inline=False
    )
    helpmsg.add_field(
        name="?compliment <name>",
        value="Generate a compliment aimed at someone",
        inline=False,
    )
    helpmsg.add_field(
        name="?level <user:optional>",
        value="Show someone's level and xp count",
        inline=False,
    )
    helpmsg.add_field(
        name="?silent", value="Stops the bot from sending random messages", inline=False
    )
    helpmsg.add_field(
        name="?mball <question>", value="Ask a question, get an answer!", inline=False
    )
    helpmsg.add_field(name="?poker", value="Start a poker game!", inline=False)
    helpmsg.add_field(name="?join", value="Join an ongoing poker game!", inline=False)
    rpgmsg = discord.Embed(title="RPG Help", description="", color=0x008800)
    rpgmsg.add_field(
        name="?trade <user> <your item id> <their item id>",
        value="Trade items with a user",
        inline=False,
    )
    rpgmsg.add_field(name="?trades", value="See your pending trades", inline=False)
    rpgmsg.add_field(name="?accept <trade id>", value="Accept a trade", inline=False)
    rpgmsg.add_field(name="?decline <trade id>", value="Decline a trade", inline=False)
    rpgmsg.add_field(
        name="?inventory [user]",
        value="See your or someone elses inventory [alias: inv]",
        inline=False,
    )
    rpgmsg.add_field(
        name="?dungeon <tier>", value="Try to fight a tiered boss", inline=False
    )
    rpgmsg.add_field(
        name="?raid [START]", value="create/join or start a raid", inline=False
    )
    rpgmsg.add_field(name="?equip <id>", value="Equip an item", inline=False)
    rpgmsg.add_field(name="?sell <id>", value="Sell an item", inline=False)
    rpgmsg.add_field(name="?sheet", value="View your character data", inline=False)
    rpgmsg.add_field(name="?origin", value="Choose an origin for your character (Lv. 5)", inline=False)
    rpgmsg.add_field(name="?evocation", value="Gain a buff as reward for leveling (Lv. 25)", inline=False)
    rpgmsg.add_field(name="?blessing", value="Gain a gods blessing as a reward for leveling (Lv. 50)", inline=False)
    rpgmsg.add_field(name="?materials", value="View how many different materials you have", inline=False)
    rpgmsg.add_field(name="?forge <type>", value="Forge a random piece of equipment based on a material (alpha, beta or gamma)", inline=False)
    adminmsg = discord.Embed(title="CN Admin commands", description="", color=0xFF0000)
    adminmsg.add_field(name="?debug", value="(ADMIN) DB debug command", inline=False)
    adminmsg.add_field(
        name="?update <@user> <amount>",
        value="(ADMIN) Give a user the provided amount",
        inline=False,
    )
    adminmsg.add_field(
        name="?filter <value>", value="(ADMIN) Filters console output.", inline=False
    )
    filters = discord.Embed(
        title="CN Filters",
        description="A list of filters for the admin console",
        color=0x0000FF,
    )
    filters.add_field(name="users", value="Toggles user messages on/off", inline=False)
    filters.add_field(name="bots", value="Toggles bot messages on/off", inline=False)
    filters.add_field(name="debug", value="Toggles debug messages on/off", inline=False)
    filters.add_field(name="all", value="Toggles all messages on", inline=False)
    filters.add_field(name="none", value="Toggles all messages off", inline=False)
    await channel.send(embed=helpmsg)
    await channel.send(embed=rpgmsg)
    if ctx.message.author.top_role.permissions.administrator:
        await channel.send(embed=adminmsg)
        await channel.send(embed=filters)


@bot.command()
async def filter(ctx, f: str):
    """
	filter: 	
			filters console messages
	Requires:
			Administrator
	"""
    global FILTER_USERS
    global FILTER_LOGS
    global FILTER_BOTS

    debug_console_log("filter", ctx.message.author, "Filter: {}".format(f))
    is_admin: bool = ctx.message.author.top_role.permissions.administrator
    if is_admin:
        f = f.lower()
        if f == "users":
            FILTER_USERS = not FILTER_USERS
            await ctx.send(
                "```Filter switched! Showing users : {}```".format(not FILTER_USERS)
            )
        elif f == "bots":
            FILTER_BOTS = not FILTER_BOTS
            await ctx.send(
                "```Filter switched! Showing bots : {}```".format(not FILTER_BOTS)
            )
        elif f == "debug":
            FILTER_LOGS = not FILTER_LOGS
            await ctx.send(
                "```Filter switched! Showing logs : {}```".format(not FILTER_LOGS)
            )
        elif f == "all":
            FILTER_USERS = False
            FILTER_BOTS = False
            FILTER_LOGS = False
            await ctx.send("```Filters switched! Now showing all messages```")
        elif f == "none":
            FILTER_USERS = True
            FILTER_BOTS = True
            FILTER_LOGS = True
            await ctx.send("```Filters switched! Now showing no messages```")
        else:
            await ctx.send("```Malformed argument - No such filter```")


@bot.command()
async def silent(ctx):
    global SILENT
    is_admin: bool = ctx.message.author.top_role.permissions.administrator
    if is_admin:
        SILENT = not SILENT
        await ctx.send("Bot silent mode: {}".format(SILENT))
    else:
        e: discord.Embed = compose_embed(0xFF0000, "CN Bot", "You dont look like an admin to me")
        await ctx.send(embed=e)


@bot.command()
async def cookie(ctx, target: discord.User):
    global DATABASE

    author = ctx.message.author
    debug_console_log("cookie", author)
    if author.id == target.id:
        e = compose_embed(
            0xFF0000, "You cant give yourself a cookie", "Even if you deserve one"
        )
        await ctx.send(embed=e)
        return
    ret = DATABASE.register(target)
    if ret != None:
        await ctx.send("```User {} has been registered!```".format(target.name))
    info = DATABASE.send_cookie(author.id, target.id)
    e = compose_embed(0xFFFFFF, "", "")
    if info == (-1, -1):
        e = compose_embed(
            0xFF0000, "Error sending cookie", "Must've been eaten on the way!"
        )
    else:
        e = compose_embed(
            0x00FF00,
            "{} sent a :cookie: to {}".format(author.name, target.name),
            ":cookie: sent: {}, :cookie: recieved: {}".format(info[0], info[1]),
        )
    await ctx.send(embed=e)


@bot.command(alias=["8ball"])
async def mball(ctx):
    response: str = random.choice(
        [
            "It is so",
            "Don't count on it",
            "Certainly so",
            "Unsure",
            "Likely so",
            "Unlikely",
        ]
    )
    e = compose_embed(0xFFFFFF, "Magic 8-ball", response)
    await ctx.send(embed=e)
    return


@bot.command()
async def slots(ctx, amount: int):
    global DATABASE
    global RIGGED

    author = ctx.message.author
    update_success: int = DATABASE.update_db(author.id, amount, True, True)
    if update_success == -1:
        e = compose_embed(
            0xFF0000, "You cant afford this bet", "We dont take monopoly money"
        )
        await ctx.send(embed=e)
        return
    debug_console_log("slots", author, "Amount: {}".format(amount))
    equivalents: dict = {
        0: ":cherries:",
        1: ":banana:",
        2: ":watermelon:",
        3: ":grapes:",
        4: ":tangerine:",
        5: ":lemon:",
    }
    # Rerolling on higher values to make it harder to win
    slot_0: int = random.randint(0, 5)
    if slot_0 > 3:
        slot_0 = random.randint(0, 5)
    slot_1: int = random.randint(0, 5)
    if slot_1 > 3:
        slot_1 = random.randint(0, 5)
    slot_2: int = random.randint(0, 5)
    if slot_2 > 3:
        slot_2 = random.randint(0, 5)
    payout_multiplier: int = 0
    if RIGGED:
        slot_0 = 5
        slot_1 = 5
        slot_2 = 5
        RIGGED = False
    if slot_0 == slot_1:
        if slot_0 == slot_2:
            payout_multiplier = slot_0 + slot_1 + slot_2
        else:
            payout_multiplier = slot_0 + slot_1
    elif slot_1 == slot_2:
        payout_multiplier = slot_1 + slot_2
    winnings: int = amount * payout_multiplier
    won: bool = winnings != 0
    e = compose_embed(
        0xFF00FF,
        "Slotmachine",
        "{} - {} - {}, you {} ¤{}!".format(
            equivalents[slot_0],
            equivalents[slot_1],
            equivalents[slot_2],
            "won" if won else "lost",
            winnings if won else amount,
        ),
    )
    await ctx.send(embed=e)
    if won:
        update_success = DATABASE.update_db(author.id, winnings, False, False)
        if update_success == -1:
            await ctx.send(
                "```diff\n-Error updating user! Please contact an administrator!\n```"
            )


@bot.command()
async def raffle(ctx, amount: int):
    global RIGGED
    global DATABASE

    author = ctx.message.author
    is_admin: bool = author.top_role.permissions.administrator
    debug_console_log("raffle", author, "Amount: {}".format(amount))
    if is_admin:
        userlist = DATABASE.get_user_list()
        winner_id: str = ""
        random.seed()
        if RIGGED:
            winner_id = str(author.id)
            RIGGED = False
        else:
            rnd = random.randint(0, len(userlist))
            winner_id = str(userlist[rnd])
        ret = DATABASE.update_db(winner_id, amount, False, False, False)
        if ret != -1:
            await ctx.send(
                "**Congratulations, <@{}>! You won ¤{} in the raffle hosted by {}!**".format(
                    winner_id, amount, author.name
                )
            )
        else:
            e = compose_embed(
                0xFF0000,
                "Error picking raffle winner!",
                "Please report this error, code: E010",
            )
            await ctx.send(embed=e)
    else:
        e = compose_embed(
            0xFF0000,
            "I dont obey plebians",
            "Get admin and then you can boss me around",
        )
        await ctx.send(embed=e)


@bot.command()
async def grab(ctx):
    """
	grab:
			if there currently is a random event, get the cash and end it
	Requires:
			Nothing
	"""
    global RANDOM_EVENT_AMOUNT
    global RANDOM_EVENT_CURRENTLY
    global DATABASE

    author = ctx.message.author
    debug_console_log("grab", author)
    if RANDOM_EVENT_CURRENTLY:
        update_success: int = DATABASE.update_db(
            author.id, RANDOM_EVENT_AMOUNT, False, False, False
        )
        if update_success != -1:
            RANDOM_EVENT_CURRENTLY = False
            e = compose_embed(
                0x00FF00,
                "Congratulations, {}!".format(author.name),
                "You have gained ¤{}".format(RANDOM_EVENT_AMOUNT),
            )
            await ctx.send(embed=e)
        else:
            e = compose_embed(
                0xFF0000, "Error", "Error updating database, contact an administrator"
            )
            await ctx.send(embed=e)
    else:
        e = compose_embed(0xFFFF00, "No event", "There is currently no event ongoing")
        await ctx.send(embed=e)


@bot.command()
async def unbox(ctx):
    """
	unbox:
			if there currently is a random event, unbox a crate and end it
	Requires:
			Nothing
	"""
    global CRATE_REWARD_AMOUNT
    global CRATE_GIVES_XP
    global RANDOM_EVENT_CURRENTLY
    global DATABASE

    author = ctx.message.author
    debug_console_log("unbox", author)
    if RANDOM_EVENT_CURRENTLY:
        update_success = 0
        if not CRATE_GIVES_XP:
            update_success = DATABASE.update_db(
                author.id, CRATE_REWARD_AMOUNT, False, False, False
            )
        else:
            update_success = DATABASE.update_db(
                author.id, CRATE_REWARD_AMOUNT, False, False, True
            )
            if update_success != -1:
                update_success = 0
        if update_success != -1:
            RANDOM_EVENT_CURRENTLY = False
            e = compose_embed(
                0xFF0000,
                "Congratulations, {}!".format(author.name),
                "You have unboxed {}{}{}".format(
                    ("¤" if not CRATE_GIVES_XP else ""),
                    CRATE_REWARD_AMOUNT,
                    ("xp" if CRATE_GIVES_XP else ""),
                ),
            )
            await ctx.send(embed=e)
            CRATE_GIVES_XP = False
        else:
            e = compose_embed(
                0xFF0000, "Error", "Error updating database, contact an administrator"
            )
            await ctx.send(embed=e)
    else:
        e = compose_embed(0xFFFF00, "No event", "There is currently no event ongoing")
        await ctx.send(embed=e)


@bot.command()
async def level(ctx, user: discord.User = None):
    """
	level:
			get your own, or somebody elses, level
	Requires:
			Nothing
	"""
    global DATABASE

    target = user
    author = ctx.message.author
    if target == None:
        target = author
    else:
        msg = DATABASE.register(target)
        if msg != None:
            await ctx.send("```User {} has been registered!```".format(target.name))
    debug_console_log(
        "level",
        author,
        "targets other: {} | target: {}".format((target != None), target),
    )
    target_xp = DATABASE.update_db(target.id, 0, False, False, True)
    tmp = target_xp
    level = 0
    while tmp > 0:
        level += 1
        tmp -= 1500 * level
    e = compose_embed(
        0xFFFFFF,
        "{}, Level {}".format(target.name, level),
        "{} has {}xp".format(target.name, target_xp),
    )
    await ctx.send(embed=e)


@bot.command(aliases=["d"])
async def daily(ctx):
    global DATABASE
    global GENERATOR
    global DAILY_BONUS

    author = ctx.message.author
    daily_success: int = DATABASE.update_daily(author.id)
    debug_console_log("daily", author, "success: {}".format(daily_success != -1))
    e = compose_embed(0xFFFFFF, "BLANK", "BLANK")
    if daily_success[0] != -1:
        e = compose_embed(
            0x00FF00,
            "{} just claimed their daily reward of {} with a streak of {} days!!".format(
                author.name, daily_success[0], daily_success[1]
            ),
            "ID: {}".format(author.id),
        )
        if random.randint(0, 10) < 6:
            item = GENERATOR.random_item(100)
            e.add_field(
                name="Neat RPG",
                value="{} was super lucky and got the item {} #{} ({}/{}/{})".format(
                    author.name,
                    item["name"],
                    item["rarity"],
                    item["ATK"],
                    item["DEF"],
                    item["LUCK"],
                ),
            )
            DATABASE.add_item(author.id, item)
    else:
        e = compose_embed(
            0xFF0000,
            "You can only claim one daily per day!",
            "ID: {}".format(author.id),
        )
    await ctx.send(embed=e)


# Roll a dice with a variable amount of sides
@bot.command(aliases=["r"])
async def roll(ctx, dice: int = 1, sides: int = 6, modifier: str = ""):
    """
	Roll: 	
			performs a riggable roll, printing the result in the chat used, utilizing the sides and dicecount provided.
	Requires:
			Nothing
	"""
    global RIGGED

    author = ctx.message.author
    debug_console_log("roll", author)
    mod: int = 0
    modiferAdds: bool = True
    if modifier != "":
        if modifier.startswith("+"):
            modiferAdds = True
            mod = int(modifier.replace("+", "").lstrip().rstrip())
        elif modifier.startswith("-"):
            modiferAdds = False
            mod = int(modifier.replace("-", "").lstrip().rstrip()) * -1
        else:
            e = compose_embed(
                0xFF0000,
                "Invalid modifier!",
                "{} is not a valid modifier".format(modifier),
            )
            await ctx.send(embed=e)
            return
    if dice == 1:
        if sides <= 1:
            # Someone will definitely attempt to roll a "0 sided die" and thats dumb
            e = compose_embed(0xFF0000, "Thats not how dice work", "")
            await ctx.send(embed=e)
            return
        roll = random.randint(1, sides)
        if RIGGED:
            # If you wanna rigg a throw, make sure it always gets the max
            e = compose_embed(
                0x00FF00,
                "You rolled a {}".format(sides + mod),
                "{}d{} {}{}".format(dice, sides, ("+" if modiferAdds else ""), mod),
            )
            await ctx.send(embed=e)
            RIGGED = False
            print('Rig successfull, returning to standard, boring "FAIR" mode.')
        else:
            e = compose_embed(
                0x00FF00,
                "You rolled a {}".format(roll + mod),
                "{}d{} {}{}".format(dice, sides, ("+" if modiferAdds else ""), mod),
            )
            await ctx.send(embed=e)
    else:
        dicerolls: list = []
        total: int = 0
        for _ in range(dice):
            if RIGGED:
                if sides > 2:
                    tmp = random.randint(sides - 1, sides)
                    dicerolls.append(tmp)
                    total += tmp
                else:
                    dicerolls.append(sides)
                    total += tmp
            else:
                tmp = random.randint(1, sides)
                dicerolls.append(tmp)
                total += tmp
        RIGGED = False
        e = compose_embed(
            0x00FF00,
            "You rolled a {}".format(total + mod),
            "{} {}d{} {}{}".format(
                dicerolls, dice, sides, ("+" if modiferAdds else ""), mod
            ),
        )
        await ctx.send(embed=e)


# Rigg the next roll
@bot.command()
async def rigg(ctx):
    """
	Rigg: 	
			riggs the next roll of any dice, regardless of source.
	Requires:
			Administrator permission, to stop users from cheating (but not admins ;))
	"""
    global RIGGED

    author = ctx.message.author
    is_admin: bool = author.top_role.permissions.administrator
    debug_console_log("rigg", author, "It'll be our little secret ;)")
    # Dont want the plebians to do this
    if is_admin:
        RIGGED = True
        # Hide the evidence
        await ctx.message.delete()
    else:
        e = compose_embed(
            0xFFFFFF,
            "How dare you!",
            "I do NOT have that kind of functionality, how dare thee!",
        )
        await ctx.send(embed=e)


# If someone were to be so incredulous as to accuse the bot
@bot.command()
async def rigged(ctx):
    """
	Rigged: 	
			accuses the bot of being rigged, which is incredibly disrespectful *cough*
	Requires:
			Nothing
	"""
    author = ctx.message.author
    debug_console_log("rigged", author)
    e = compose_embed(
        0xFFFFFF,
        "How dare you!",
        "I do NOT have that kind of functionality, how dare thee!",
    )
    await ctx.send(embed=e)


# Dice game, most of the code is DB stuff
@bot.command(aliases=["55x2", "g", "bet"])
async def gamble(ctx, bet: int = 0):
    """
	gamble: 	
			rolls a 100-sided die with a provided bet, and pays out double if above 55.
	Requires:
			User must be registered and have a sufficient balance to play the game
	"""
    global RIGGED
    global DATABASE

    author = ctx.message.author
    if bet <= 0:
        e = compose_embed(
            0xFF0000,
            "You must supply a bet",
            "Even if these tokens dont really exist, I cant accept an empty bet!",
        )
        await ctx.send(embed=e)
        debug_console_log("gamble", author, "Malformed command argument")
        return
    # get the current userid (db stuff)
    if RIGGED:
        # make sure we win if its rigged
        roll = random.randint(55, 100)
        # debug info
        RIGGED = False
    else:
        # fair and boring roll
        roll = random.randint(1, 100)
        # debug info
    update_success: int = 0
    debug_console_log("gamble", author, "¤{} | Won: {}".format(bet, roll > 55))
    if roll <= 55:
        update_success = DATABASE.update_db(author.id, int(bet), True)
        if update_success != -1:
            e = compose_embed(
                0x0000FF,
                "I'm sorry, you just lost ¤{}!".format(bet),
                "Needed: >55. Got: {}".format(roll),
            )
            await ctx.send(embed=e)
            return
        else:
            e = compose_embed(
                0xFF0000,
                "Insufficient account balance",
                "You cant bet money you dont have!",
            )
            await ctx.send(embed=e)
            return
    else:
        update_success = DATABASE.update_db(author.id, int(bet), False)
        if update_success != -1:
            e = compose_embed(
                0x00FF00,
                "Congratulations! You just won ¤{}".format(bet),
                "Needed: >55. Got: {}".format(roll),
            )
            await ctx.send(embed=e)
            return
        else:
            e = compose_embed(
                0xFF0000,
                "Insufficient account balance",
                "You cant bet money you dont have!",
            )
            await ctx.send(embed=e)
            return


@bot.command()
async def sarcasm(ctx):
    """
    Sarcasm: 
        Make a message explicitly sarcastic for all of those who dont get jokes
    Requires:
        A message to make sarcastic
    """
    author = ctx.message.author
    debug_console_log("sarcasm", author, "")
    msg: str = ctx.message.content.replace("?sarcasm ", "")
    retmsg: str = ""
    for char in msg:
        retmsg += char.upper() if random.randint(0, 1) == 1 else char.lower()
    await ctx.send("```{}```".format(retmsg))
    return


@bot.command()
async def roulette(ctx, bet: str = "", amount: int = 0):
    """
    Roulette:
        A miniature roulette wheel, with some of the bets supported (TODO: Several bets per roll [*bets > bet], support more bet types)
    Requires:
        Being registered in the database, and enough money to field the bet
    """
    global DATABASE

    author = ctx.message.author
    # Tell the user what to do if they dont supply any arguments
    debug_console_log("roulette", author, "Bet: {} | Amount: ¤{}".format(bet, amount))
    if bet == "" and amount == 0:
        e = compose_embed(0xFF00FF, "Roulette", "Possible bets:")
        e.add_field(
            name="Red",
            value="Bet on whether the roll is a red number, x2 win",
            inline=False,
        )
        e.add_field(
            name="Black",
            value="Bet on whether the roll is a black number, x2 win",
            inline=False,
        )
        e.add_field(
            name="Even",
            value="Bet on whether the roll is an even number, x2 win",
            inline=False,
        )
        e.add_field(
            name="Odd",
            value="Bet on whether the roll is an odd number, x2 win",
            inline=False,
        )
        e.add_field(
            name="Low",
            value="Bet on whether the roll is at or below 18, x2 win",
            inline=False,
        )
        e.add_field(
            name="High",
            value="Bet on whether the roll is at or above 19, x2 win",
            inline=False,
        )
        e.add_field(
            name="Col1",
            value="Bet on whether the roll is in column 1, x3 win",
            inline=False,
        )
        e.add_field(
            name="Col2",
            value="Bet on whether the roll is in column 2, x3 win",
            inline=False,
        )
        e.add_field(
            name="Col3",
            value="Bet on whether the roll is in column 3, x3 win",
            inline=False,
        )
        e.add_field(
            name="Zero",
            value="Bet on whether the roll is an exact 0, x50 win",
            inline=False,
        )
        await ctx.send(embed=e)
        return
    b: str = bet.lower()  # Make sure that RED reD red, etc, are all handled the same
    valid_bets: list = [
        "red",
        "black",
        "even",
        "odd",
        "low",
        "high",
        "col1",
        "col2",
        "col3",
        "zero",
    ]
    if b not in valid_bets:  # Ignore invalid bets
        e = compose_embed(0xFF0000, "Roulette", "Error: No such bet")
        await ctx.send(embed=e)
        return
    if amount <= 0:  # Ignore non-existant bets
        e = compose_embed(0xFF0000, "Roulette", "Error: Cannot bet nothing")
        await ctx.send(embed=e)
        return
    author_balance: int = DATABASE.update_db(author.id, 0, False)
    if author_balance == -1:  # Check that the user is properly registered
        e = compose_embed(0xFF0000, "Roulette", "Error: Could not access database")
        await ctx.send(embed=e)
        return
    if author_balance < amount:  # Check that they have enough money to play
        e = compose_embed(
            0xFF0000, "Roulette", "Error: You dont have enough to make a bet that big!"
        )
        await ctx.send(embed=e)
        return
    tmp = DATABASE.update_db(author.id, amount, True)
    if (
        tmp == -1
    ):  # Make sure that we can subtract the bet from their account, then do so
        e = compose_embed(0xFF0000, "Roulette", "Error: Could not access database")
        await ctx.send(embed=e)
        return
    # Lists for easy bet-win checks
    roll = random.randint(0, 36)
    red_numbers: list = [
        1,
        3,
        5,
        7,
        9,
        12,
        14,
        16,
        18,
        19,
        21,
        23,
        25,
        27,
        30,
        32,
        34,
        36,
    ]
    col1: list = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    col2: list = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    winnings: int = 0
    if b == "red":  # God I miss switch { case: } statements
        if roll in red_numbers:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :red_circle:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :black_circle:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "black":  # God I miss switch { case: } statements
        if roll not in red_numbers:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :black_circle:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :red_circle:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "even":  # God I miss switch { case: } statements
        if roll % 2 == 0:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :performing_arts:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :performing_arts:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "odd":  # God I miss switch { case: } statements
        if roll % 2 != 0:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :performing_arts:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :performing_arts:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "low":  # God I miss switch { case: } statements
        if roll <= 18:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :arrow_down:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :arrow_up:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "high":  # God I miss switch { case: } statements
        if roll >= 19:
            winnings = amount * 2
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :arrow_up:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :arrow_down:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "col1":  # God I miss switch { case: } statements
        if roll in col1:
            winnings = amount * 3
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :one:".format(winnings, roll),
                )
                await ctx.send(embed=e)
                return
        else:
            column: int = 0
            if roll in col2:
                column = 2
            else:
                column = 3
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :{}:".format(
                    amount, roll, "two" if column == 2 else "three"
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "col2":  # God I miss switch { case: } statements
        if roll not in red_numbers:
            winnings = amount * 3
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :two:".format(winnings, roll),
                )
                await ctx.send(embed=e)
                return
        else:
            column: int = 0
            if roll in col1:
                column = 1
            else:
                column = 3
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :{}:".format(
                    amount, roll, "one" if column == 1 else "three"
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "col3":  # God I miss switch { case: } statements
        if roll in red_numbers:
            winnings = amount * 3
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :three:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            column: int = 0
            if roll in col1:
                column = 1
            else:
                column = 2
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :{}:".format(
                    amount, roll, "one" if column == 1 else "two"
                ),
            )
            await ctx.send(embed=e)
            return
    if b == "zero":  # God I miss switch { case: } statements
        if roll == 0:
            winnings = amount * 50
            bal = DATABASE.update_db(author.id, winnings, False, False)
            if bal == -1:
                e = compose_embed(
                    0xFF0000, "Roulette", "Error: Could not access database"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0x00FF00,
                    "Roulette",
                    "Congratulations! You won ¤{} on [{}] :zero:".format(
                        winnings, roll
                    ),
                )
                await ctx.send(embed=e)
                return
        else:
            e = compose_embed(
                0xFF9900,
                "Roulette",
                "Sorry! You lost ¤{}, the roll was [{}] :slight_frown:".format(
                    amount, roll
                ),
            )
            await ctx.send(embed=e)
            return


# Show a user their balance
@bot.command(aliases=["money", "balance", "eco"])
async def bal(ctx, user: discord.User = None):
    """
	Bal: 	
			responds with the users balance.
	Requires:
			user must be registered
	"""
    global DATABASE

    author = ctx.message.author
    target_name = ""
    balance = 0
    if user == None:
        balance = DATABASE.update_db(author.id, 0, False, False)
        target_name = author.name
    else:
        balance = DATABASE.update_db(user.id, 0, False, False)
        if balance == -1:
            DATABASE.register(user)
            balance = 1000
        target_name = user.name
    e = compose_embed(
        0x00FF00, "{} has ¤{}".format(target_name, balance), "ID: {}".format(author.id)
    )
    await ctx.send(embed=e)


@bot.command(aliases=["lotto", "l"])
async def lottery(ctx):
    global DATABASE
    global LOTTO_REWARD

    random.seed()
    win = random.randint(0, 1000)
    random.seed()
    rnd = random.randint(0, 1000)
    author = ctx.message.author
    author_cash = DATABASE.update_db(author.id, 0, False, False, False)
    if author_cash > 100:
        DATABASE.update_db(author.id, 100, True, True)
    else:
        e = compose_embed(0xFF0000, "You cant afford a ticket!", "They cost ¤100")
        await ctx.send(embed=e)
        return
    debug_console_log(
        "lottery", author, "Winning number: {} - Drawn number: {}".format(win, rnd)
    )
    if win == rnd:
        DATABASE.update_db(author.id, LOTTO_REWARD, False, False, False)
        e = compose_embed(
            0x00FF00,
            "Congratulations! You won ¤{} with insane luck!".format(LOTTO_REWARD),
            "Seriously, thats insane",
        )
        await ctx.send(embed=e)
        return
    else:
        e = compose_embed(
            0xFF0000,
            "Better luck next time!",
            "Dont be discouraged, the chance is insanely low",
        )
        await ctx.send(embed=e)
        return


@bot.command()
async def bw(ctx, shade: str, dice: int):
    shade_color: str = shade.upper()
    shade_dice: int = dice
    if shade_color not in ["B", "W", "G"]:
        e = compose_embed(
            0xFF0000, "Invalid shade", "{} is not a valid shade".format(shade_color)
        )
        await ctx.send(embed=e)
        return
    if shade_dice < 1:
        e = compose_embed(
            0xFF0000, "No dice to roll", "Did you format the command correctly?"
        )
        await ctx.send(embed=e)
        return
    rolls: list = []
    for _ in range(shade_dice):
        rolls.append(random.randint(1, 6))
    output: discord.Embed = discord.Embed(
        title="Burning Wheel",
        description="{} {}".format(shade_color, shade_dice),
        color=0x000000,
    )
    successes: int = 0
    failures: int = 0
    for roll in rolls:
        if shade_color == "B":
            if roll > 3:
                output.add_field(
                    name="Roll: {}".format(roll), value="Success!", inline=False
                )
                successes += 1
            else:
                output.add_field(
                    name="Roll: {}".format(roll), value="Failure!", inline=False
                )
                failures += 1
        if shade_color == "G":
            if roll > 2:
                output.add_field(
                    name="Roll: {}".format(roll), value="Success!", inline=False
                )
                successes += 1
            else:
                output.add_field(
                    name="Roll: {}".format(roll), value="Failure!", inline=False
                )
                failures += 1
        if shade_color == "W":
            if roll > 1:
                output.add_field(
                    name="Roll: {}".format(roll), value="Success!", inline=False
                )
                successes += 1
            else:
                output.add_field(
                    name="Roll: {}".format(roll), value="Failure!", inline=False
                )
                failures += 1
    output.add_field(
        name="Successes: {}".format(successes),
        value="Failures: {}".format(failures),
        inline=False,
    )
    await ctx.send(embed=output)


# Get some debug info in the console
@bot.command()
async def debug(ctx):
    """
	Debug: 	
			prints the current db state and global information to the console, to aid in troubleshooting
			db issues.
	Requires:
			Administrator permission, to stop users from spamming the console with debug info
	"""
    global DATABASE

    author = ctx.message.author
    is_admin: bool = author.top_role.permissions.administrator
    debug_console_log("debug", author)
    # I really dont want people to spam debug info
    if is_admin:
        DATABASE.print_internal_state()
        e = compose_embed(
            0x00FF00,
            "Information on the internal state sent to the console!",
            "ID: {}".format(author.id),
        )
        await ctx.send(embed=e)
    else:
        e = compose_embed(
            0xFF0000,
            "Permission error",
            "This command requires Administrator priviliges",
        )
        await ctx.send(embed=e)


# Change someones balance
@bot.command()
async def update(ctx, user: discord.User, amount: int):
    """
	Update: 	
			gives the specified user <amount> extra ¤.
	Requires:
			Administrator permission, for what i hope is an obvious reason. User must also be registered
	"""
    global DATABASE

    author = ctx.message.author
    msg = DATABASE.register(user)
    if msg != None:
        await ctx.send("```User {} has been registered!```".format(user.name))
    is_admin: bool = author.top_role.permissions.administrator
    debug_console_log(
        "update",
        author,
        "Target: ({}) {}, update amount: ¤{}".format(user.id, user.name, amount),
    )
    # I really dont want normal people to do this
    if is_admin:
        update_success: int = DATABASE.update_db(user.id, amount, False, False)
        if update_success != -1:
            e = compose_embed(
                0xFF00FF,
                "Added ¤{} to {}'s balance!".format(amount, user.name),
                "ID: {}".format(user.id),
            )
            await ctx.send(embed=e)
            return
        else:
            e = compose_embed(
                0xFF0000,
                "Cannot update a user who isnt registered!",
                "ID: {}".format(user.id),
            )
            await ctx.send(embed=e)
            return
    else:
        e = compose_embed(
            0xFF0000,
            "Permission error",
            "This command requires Administrator priviliges",
        )
        await ctx.send(embed=e)


@bot.command(aliases=["s", "rob", "thieve"])
async def steal(ctx, target: discord.User):
    """
    Steal:
            Take 10-20% of a targets money with a 3% chance of success and a fine on failure
    Requires:
            A target to steal from
    """
    global DATABASE
    global FINE_AMOUNT

    author = ctx.message.author
    if author.id == target.id:
        e = compose_embed(
            0xFF0000,
            "You cant steal from yourself",
            "Unless you're mentally ill in which case I apologize",
        )
        await ctx.send(embed=e)
        return
    if target.bot:
        e = compose_embed(
            0xFF0000,
            "Bots dont have money",
            "They're equally offended at your attempt however",
        )
        await ctx.send(embed=e)
        return
    theft_successful: bool = False
    tmp = DATABASE.update_user_thefts(author.id, False, True)
    if tmp > 10:
        e = compose_embed(
            0xFF0000,
            "You must bribe to be able to steal again",
            "Wouldnt want you to abuse this, hm?",
        )
        await ctx.send(embed=e)
        return
    random.seed()
    r = random.randint(0, 100)
    if r < 3:
        theft_successful = True
    debug_console_log("steal", author, "Success: {}".format(theft_successful))
    if theft_successful:
        target_money: int = DATABASE.update_db(target.id, 0, False, False)
        stolen_amount: int = int(target_money * (random.randint(10, 20) / 100))
        tmp = DATABASE.update_db(target.id, stolen_amount, True, False)
        tmp = DATABASE.update_db(author.id, stolen_amount, False, False)
        e = compose_embed(
            0x00FF00,
            "{} successfully stole ¤{} from {}!".format(
                author.name, stolen_amount, target.name
            ),
            "AID: {} - TID: {}".format(author.id, target.id),
        )
        await ctx.send(embed=e)
        return
    else:
        failed_thefts: int = DATABASE.update_user_thefts(author.id)
        if failed_thefts <= 10:
            fine: int = FINE_AMOUNT * failed_thefts
            author_money: int = DATABASE.update_db(author.id, 0, False, False)
            if fine > author_money:
                DATABASE.update_db(author.id, author_money, True, False)
                while failed_thefts <= 10:
                    failed_thefts = DATABASE.update_user_thefts(author.id)
                e = compose_embed(
                    0xFF0000,
                    "Stop right there, criminal scum!",
                    "You couldn't affort the fine and were thrown in prison.",
                )
                await ctx.send(embed=e)
                return
            tmp = DATABASE.update_db(author.id, fine, True, False)
            if tmp < 0:
                tmp = DATABASE.update_db(author.id, tmp, True, False)
            e = compose_embed(
                0xFF0000,
                "Stop right there, criminal scum!",
                "You have paid a fine of ¤{}".format(fine),
            )
            await ctx.send(embed=e)
            return
        else:
            author_money: int = DATABASE.update_db(author.id, 0, False, False)
            tmp = DATABASE.update_db(author.id, int(author_money * 0.9), True, False)
            e = compose_embed(
                0xFF0000,
                "Stop right there, criminal scum!",
                "You were thrown in jail, losing 90% of your money!",
            )
            await ctx.send(embed=e)
            return


@bot.command()
async def bribe(ctx):
    """
    Bribe:
            Pay off the court to avoid a prison sentence after 10 thefts
    Requires:
            Enough money to bribe them
    """
    global DATABASE
    global BRIBE_PRICE

    author = ctx.message.author
    author_money: int = DATABASE.update_db(author.id, 0, False, False)
    price: int = DATABASE.update_user_thefts(author.id, False, True) * BRIBE_PRICE
    if author_money < price:
        e = compose_embed(
            0xFFFF00,
            "You need ¤{} to bribe but you only have ¤{}".format(price, author_money),
            "Better hit the casino!",
        )
        await ctx.send(embed=e)
        return
    else:
        DATABASE.update_db(author.id, price, True, False)
        DATABASE.update_user_thefts(author.id, True)
        e = compose_embed(
            0x00FF00,
            "You paid a bribe of ¤{} and are now no longer a know thief".format(price),
            "The Thieves guild would be so proud",
        )
        await ctx.send(embed=e)
        return


@bot.command(aliases=["give"])
async def pay(ctx, user: discord.User, amount: int):
    """
	Pay:
			Give another user money from your own balance.
	Requires:
			The user to pay, the amount to pay, and a balance that covers the amount.
	"""
    global DATABASE

    user_from = ctx.message.author
    user_to = user
    if user_from == user_to:
        e = compose_embed(
            0xFF0000,
            "Giving yourself an allowance is weird, man",
            "C'mon, you're better than this",
        )
        await ctx.send(embed=e)
        return
    if amount < 0:
        e = compose_embed(
            0xFF0000, "You cant give debt.", "The authorities have been alerted."
        )
        await ctx.send(embed=e)
        print("=================================================")
        print("{} Attempted to steal from {}".format(user_from.name, user_to.name))
        print("=================================================")
        return
    if user_to.bot:
        e = compose_embed(0xFF0000, "Bots dont have money, silly", "C'mon")
        await ctx.send(embed=e)
        return
    msg = DATABASE.register(user_to)
    if msg != None:
        await ctx.send("```User {} has been registered!```".format(user_to.name))
    debug_console_log(
        "pay",
        user_from,
        "Target: ({}) {}, amount: ¤{}".format(user_to.id, user_to.name, amount),
    )
    update_success_deduct: int = DATABASE.update_db(user_from.id, amount, True)
    if update_success_deduct != -1:
        update_success_increase: int = DATABASE.update_db(
            user_to.id, amount, False, False
        )
        if update_success_increase != -1:
            e = compose_embed(
                0x00FF00,
                "Sucessfully sent ¤{} to {}!".format(amount, user_to.name),
                "FROM: {} - TO: {}".format(user_from.id, user_to.id),
            )
            await ctx.send(embed=e)
            return
        else:
            update_success_reset: int = DATABASE.update_db(
                user_from.id, amount, False, False
            )
            if update_success_reset != -1:
                e = compose_embed(
                    0xFF0000, "Error during transfer", "You have not been charged"
                )
                await ctx.send(embed=e)
                return
            else:
                e = compose_embed(
                    0xFF0000,
                    "Error during transfer",
                    "You have been charged, contact an administrator!",
                )
                await ctx.send(embed=e)
                return
    else:
        e = compose_embed(
            0xFF0000, "Error during transfer", "You cant give more than you have!"
        )
        await ctx.send(embed=e)
        return


@bot.command()
async def order(ctx, drink: str = "empty"):
    """
	Order:
			Order a functionally non-existant drink with no effects.
	Requires:
			Enough money to buy the required drink, aswell as the drink to buy.
	"""
    global DATABASE

    author = ctx.message.author
    debug_console_log("order", author, "Drink: {}".format(drink))
    # Dict would be preferable but I'm tired and just want to iterate
    drinks: list = ["beer", "cider", "wine", "vodka", "rum", "cognac", "whiskey"]
    prices: list = [500, 1000, 2500, 5000, 10000, 15000, 30000]
    if drink == "empty":
        e = discord.Embed(title="CN Bot", description="", color=0x662200)
        e.add_field(
            name="What can I getcha?", value="I currently have ...", inline=False
        )
        i = 0
        while i < (len(drinks)):
            e.add_field(name=str(drinks[i]), value=str(prices[i]), inline=False)
            i += 1
        await ctx.send(embed=e)
    else:
        if drink.lower() in drinks:
            price = prices[drinks.index(drink.lower())]
            randxp: int = random.randint(
                price / 10 - (price / 100), price / 10 + (price / 100)
            )
            update_success: int = DATABASE.update_db(author.id, price, True)
            update_xp: int = DATABASE.update_db(author.id, randxp, False, False, True)
            if update_success != -1 and update_xp != -1:
                e = compose_embed(
                    0xFFFFFF,
                    "You buy a glass of {}".format(drink.lower()),
                    "You gain {}xp!".format(randxp),
                )
                await ctx.send(embed=e)
            else:
                e = compose_embed(
                    0xFF0000, "You cant afford that.", "I dont take imaginary currency"
                )
                await ctx.send(embed=e)
        else:
            e = compose_embed(
                0xFF0000, "You cant afford that.", "I dont take imaginary currency"
            )
            await ctx.send(embed=e)


@bot.command()
async def insult(ctx, *args):
    """
	Insult:
			Insult someone by name.
	Requires:
			Some(one/thing) to insult
	"""
    author = ctx.message.author
    name: str = ""
    for arg in args:
        name += str(arg)
        name += " "
    name = name.rstrip()
    debug_console_log("insult", author, "Target: {}".format(name))
    # Insults are composed in the pattern (P N F), where the name N is provided to the function.
    # Adding insults to the preamble P and finisher F lists, will result in more diverse insults.
    # Make sure to add them according to the already established pattern.
    preambles: list = [
        "Why dont you choke on an icecube, ",
        "I can see why you were abandoned as a kid, ",
        "I hope you melt in the sun like the snowflake you are, ",
        "If there ever was a reason to sue the company that made your dad's condom, it would be you, ",
        "Honestly, I'd rather pet a putrid furry than stand within 30 ft. of you, ",
        "Its ok, if I were you I'd be sad too, ",
        "The landfill you were born in deserves a refund, ",
        "I sure hope there ain't a God, cause wow he hates us if he let you step foot on this earth, ",
    ]
    plen: int = len(preambles) - 1
    finishers: list = [
        ", you're the reason aliens wont visit us.",
        ", hope you weren't vaccinated.",
        ", you quaking soyboy.",
        ", damn disgrace.",
        ", they use your face for chastity propaganda.",
        ", trashlord.",
        ", bloated dumpsterkid.",
        ", you sad, failed abortion.",
        ", its like you rolled a nat 1 on life.",
    ]
    flen: int = len(finishers) - 1
    pidx: int = random.randint(0, plen)
    fidx: int = random.randint(0, flen)
    msg: str = (preambles[pidx] + name + finishers[fidx])
    e = compose_embed(0xFF00FF, msg, "ID: {}".format(author.id))
    await ctx.send(embed=e)


@bot.command()
async def compliment(ctx, *args):
    """
	Compliment:
			Compliment someone by name.
	Requires:
			Some(one/thing) to compliment
	"""
    author = ctx.message.author
    name: str = ""
    for arg in args:
        name += str(arg)
        name += " "
    name = name.rstrip()
    debug_console_log("compliment", author, "Target: {}".format(name))
    # Compliments are composed just like insults are.
    preambles: list = [
        "I hope you've had a wonderful day, ",
        "Your parents love you, and even if they dont, I sure do, ",
        "You're the standard others strive to reach, ",
        "I'm glad you exist, ",
        "Hugging through cyberspace is kinda hard, but you'd deserve it ",
        "I wish I was as cool as you, ",
        "You're the gift that keeps on giving, ",
        "You might be the closest we've ever come to irrefutable evidence that there is a benevolent God out there, ",
    ]
    plen: int = len(preambles) - 1
    finishers: list = [
        ", you light up the room.",
        ", hope you were vaccinated.",
        ", you're pretty neat.",
        ", I'm so proud of you.",
        ", your personality is magnetic.",
        ", you must've rolled a nat 20 on life.",
        ", I love your company!",
        ", I wish you the best!",
    ]
    flen: int = len(finishers) - 1
    pidx: int = random.randint(0, plen)
    fidx: int = random.randint(0, flen)
    msg: str = (preambles[pidx] + name + finishers[fidx])
    e = compose_embed(0xFF00FF, msg, "ID: {}".format(author.id))
    await ctx.send(embed=e)


@bot.command()
async def sadviolinnoises(ctx):
    message: str = "Ok man. I guess you don't really matter to me. Good luck what what ever you continue on to do and I hope you have a wonderful life. It seems at this point we must diverge, it seems like we don't really seem to have anything in common to talk about and so it would be best to just no longer pretend to care about each other. Thank you for being honest with your statement since it's be an issue I have not been sure how to deal with properly up until now. I guess I have been a shitty person for not being able to take a moment out of my sleepless nights to contact you so if my short coming on that regard has offended you in any way shape or form I do apologize. To address any possible returning statements, as once I have sent this message based on your prior statement it seems that my best course of action is to cut contact, you seem to state talking like penguin is an issue and insinuated that I spoke like an over exaugurated version of him. This message has been formatted to how our current stance is as we shall now define it as at best acquaintances, as I have emotionally distanced myself from you at this point I have resorted to formal speech since that is just who I am. Ridicule it if you so wish, at this point it seems that you no longer wish for me to be around anymore so that will be arranged. Do not worry about any personal information you have disclosed being leaked out. As my nature dictates me I tend to try and keep information given to me in confidence as such. It is unlikely any thing which I have screen shot or remember from our past conversations will be brought up by me in any place. Since it is likely you will share this conversation with Manis as we often have done in the past. I also advice him to let me know if he wants to formalize this cutting of contact to ensure no awkward conversations that neither of us desire such as this occurs again. Again I wish the both of you the best of luck and thank you for being honest with me. Good night."
    await ctx.send("```{}```".format(message))


@bot.command()
async def poker(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        GAME.new_game()
        GAME.add_player(ctx.author)
        GAME.state = GameState.WAITING
        e: discord.Embed = compose_embed(
            0x00FF00,
            "Poker Game",
            "A new poker game was just created by {}!".format(ctx.author.name),
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "A game has already been made! {}".format(
                "You can join it with ?join" if GAME.state == GameState.WAITING else ""
            ),
        )
        await ctx.send(embed=e)


@bot.command()
async def join(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "There is currently no game to join! Message ?poker to make one!",
        )
        await ctx.send(embed=e)
        return
    if GAME.state != GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Game is currently in progress, you cant join!"
        )
        await ctx.send(embed=e)
        return
    if GAME.add_player(ctx.author):
        e: discord.Embed = compose_embed(
            0x00FF00, "Poker Game", "{} just joined the game!".format(ctx.author.name)
        )
        await ctx.send(embed=e)
        return
    e: discord.Embed = compose_embed(
        0xFF0000, "Poker Game", "You cant join a game you're already in!"
    )
    await ctx.send(embed=e)


@bot.command()
async def start(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "You cant start a game that hasnt been made yet! ?poker",
        )
        await ctx.send(embed=e)
        return
    if GAME.state != GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Game is already started!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You're not in the game! ?join"
        )
        await ctx.send(embed=e)
        return
    if len(GAME.players) < 2:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You need atleast 2 players to play"
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.start()))


@bot.command()
async def deal(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You cant deal if there isnt a game"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You need to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state != GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have already dealt for this round"
        )
        await ctx.send(embed=e)
        return
    if GAME.dealer.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "You arent the dealer, please wait for {} to ?deal".format(
                GAME.dealer.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.deal_hands()))
    for player in GAME.players:
        cards = player.cards
        if player.user.dm_channel == None:
            await player.user.create_dm()
        channel = player.user.dm_channel
        suit_translate: dict = {
            "♠": "Spade",
            "♥": "Heart",
            "♦": "Diamond",
            "♣": "Clover",
        }
        await channel.send(
            "================================\nYour cards:\n{}{}({}) / {}{}({})\n================================".format(
                cards[0].suit,
                cards[0].rank,
                suit_translate[cards[0].suit],
                cards[1].suit,
                cards[1].rank,
                suit_translate[cards[1].suit],
            )
        )


@bot.command()
async def call(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Theres currently not a game going on! ?poker"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to be in the game to call!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Cards havent been dealt yet, calm down!"
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Its currently {}'s turn, you cant call yet".format(
                GAME.current_player.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.call()))


@bot.command()
async def check(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Theres currently not a game going on! ?poker"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to be in the game to check!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Cards havent been dealt yet, calm down!"
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Its currently {}'s turn, you cant check yet".format(
                GAME.current_player.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.cur_bet != GAME.cur_bet:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "You cant check yet, you have only bet ${} out of ${}".format(
                GAME.current_player.cur_bet, GAME.cur_bet
            ),
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.check()))


@bot.command(aliases=["raise"])
async def raise_bet(ctx, amount: int):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Theres currently not a game going on! ?poker"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to be in the game to raise!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Cards havent been dealt yet, calm down!"
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Its currently {}'s turn, you cant raise yet".format(
                GAME.current_player.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    try:
        if GAME.cur_bet >= GAME.current_player.max_bet:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Poker Game",
                "You dont have enough money to raise the current bet of ${}".format(
                    GAME.cur_bet
                ),
            )
            await ctx.send(embed=e)
            return
        if GAME.cur_bet + amount > GAME.current_player.max_bet:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Poker Game",
                "You dont have enough money to raise by ${}, the most you can raise by is ${}".format(
                    amount, GAME.current_player.max_bet - GAME.cur_bet
                ),
            )
            await ctx.send(embed=e)
            return
        await ctx.send("\n".join(GAME.raise_bet(amount)))
    except ValueError:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Please raise by an integer amount"
        )
        await ctx.send(embed=e)
        return


@bot.command()
async def fold(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Theres currently not a game going on! ?poker"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to be in the game to fold!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Cards havent been dealt yet, calm down!"
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Its currently {}'s turn, you cant fold yet".format(
                GAME.current_player.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.fold()))


@bot.command()
async def chips(ctx):
    global GAME
    if GAME.state in (GameState.NO_GAME, GameState.WAITING):
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "You cant request the chip count before the game has begun",
        )
        await ctx.send(embed=e)
        return
    message: str = ""
    for player in GAME.players:
        message += "{} has ${}\n".format(player.user.name, player.balance)
    e: discord.Embed = compose_embed(0xFF00FF, "Poker Game", message)
    await ctx.send(embed=e)


@bot.command()
async def allin(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Theres currently not a game going on! ?poker"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.WAITING:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to start the game first!"
        )
        await ctx.send(embed=e)
        return
    if not GAME.is_player(ctx.author):
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "You have to be in the game to go all in!"
        )
        await ctx.send(embed=e)
        return
    if GAME.state == GameState.NO_HANDS:
        e: discord.Embed = compose_embed(
            0xFF0000, "Poker Game", "Cards havent been dealt yet, calm down!"
        )
        await ctx.send(embed=e)
        return
    if GAME.current_player.user != ctx.author:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Its currently {}'s turn, you cant go all in yet".format(
                GAME.current_player.user.name
            ),
        )
        await ctx.send(embed=e)
        return
    await ctx.send("\n".join(GAME.all_in()))


@bot.command()
async def endgame(ctx):
    global GAME
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        GAME.players = []
        if GAME.state == GameState.WAITING:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Poker Game",
                "Game ended before it began. Make up your mind before you waste my time alright?",
            )
            await ctx.send(embed=e)
        elif GAME.state in (GameState.NO_HANDS, GameState.HANDS_DEALT):
            e: discord.Embed = compose_embed(
                0xFF0000, "Poker Game", "Fun's over! Nothing to see here, people!"
            )
            await ctx.send(embed=e)
        elif GAME.state in (
            GameState.FLOP_DEALT,
            GameState.TURN_DEALT,
            GameState.RIVER_DEALT,
        ):
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Poker Game",
                "Fun's over! Put down that deck of cards! Don't you dare deal anything!",
            )
            await ctx.send(embed=e)
        else:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Poker Game",
                "You just tried to end a game that wasnt even started yet, didnt you? Monster.",
            )
            await ctx.send(embed=e)
        GAME.state = GameState.NO_GAME
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Poker Game",
            "Nice try {}, but you dont look like an admin to me, and I dont take orders from plebs.".format(
                ctx.author.name
            ),
        )
        await ctx.send(embed=e)


@bot.command()
async def leave(ctx):
    global GAME
    if GAME.state == GameState.NO_GAME:
        await ctx.send("Theres no game to leave!")
    else:
        usr = ctx.author.name
        i = 0
        while i < len(GAME.players):
            player = GAME.players[i]
            if player.user.name == usr:
                GAME.players.pop(i)
                if len(GAME.players) == 0:
                    GAME.players = []
                    GAME.state = GameState.NO_GAME
                    await ctx.send(
                        "Congrats, you just killed a game you started for no reason! Have you no consideration for the cycles you just wasted?"
                    )
                if len(GAME.players) > 1:
                    GAME.pot.handle_fold(player)
                    GAME.leave_hand(player)
                    try:
                        if GAME.turn_index > len(GAME.in_hand):
                            GAME.turn_index = len(GAME.in_hand) - 1
                        if GAME.dealer_index > len(GAME.players):
                            GAME.dealer_index = len(GAME.players) - 1
                    except:
                        print(
                            "******************[!] EXCEPTION TRYING TO SET INDICES [!]******************"
                        )
                    await ctx.send(
                        "**{}** Dropped out!\n**{}** is dealer and its **{}'s** turn!\n".format(
                            usr,
                            GAME.players[GAME.dealer_index].user.mention,
                            GAME.in_hand[GAME.turn_index].user.mention,
                        )
                    )
                elif len(GAME.players) == 1:
                    if GAME.state == GameState.WAITING:
                        GAME.state = GameState.NO_GAME
                        await ctx.send(
                            "Woops! Looks like **{}** dosen't wanna play after all!".format(
                                usr
                            )
                        )
                    else:
                        GAME.state = GameState.NO_GAME
                        await ctx.send(
                            "**{}** wins the game due to the forfeit of {}".format(
                                GAME.players[0].user.mention, usr
                            )
                        )
            else:
                i += 1
        await ctx.send("You're not even in the game {}".format(ctx.author.mention))


@bot.command(aliases=["lb"])
async def leaderboard(ctx, ranking: str = ""):
    global DATABASE
    rankings: list = ["xp", "balance", "cookies"]
    if ranking not in rankings:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Leaderboard",
            "Please provide one of the following ranking qualifiers",
        )
        for rank in rankings:
            e.add_field(name="Ranking", value=rank, inline=False)
        await ctx.send(embed=e)
        return
    if ranking == "cookies":
        ranking = "cookies_got"
    users: list = DATABASE.get_users()
    users.sort(key=lambda user: int(user.getprop(ranking)), reverse=True)

    e: discord.Embed = compose_embed(
        0xFFFF00,
        "{} Leaderboard".format(ranking),
        "Users registered: {}".format(len(users)),
    )
    placement: int = 1
    for user in users:
        u = ctx.message.guild.get_member(int(user.getprop("id")))
        e.add_field(
            name="({}):\t{}, Level {}".format(placement, u.name, user.getprop("level")),
            value="{}{} {}".format(
                "¤" if ranking == "balance" else "",
                user.getprop(ranking),
                ranking.replace("_got", "") if ranking != "balance" else "",
            ),
            inline=False,
        )
        placement += 1
    await ctx.send(embed=e)


@bot.command()
async def dungeon(ctx, dungeon_level: int = -1):
    global DATABASE
    global GENERATOR
    if dungeon_level < 0 or dungeon_level > 20:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "Please choose a dungeon between 0 and 20!"
        )
        await ctx.send(embed=e)
        return
    item = None
    boss = GENERATOR.generate_boss(dungeon_level)
    char = DATABASE.get_character(ctx.author.id)
    success: bool = (
        (int(char["LV"]) - dungeon_level * 10)
        + (int(char["ATK"]) - int(boss["DEF"]))
        - (int(boss["ATK"]) - int(char["DEF"]))
    ) + (int(char["LUCK"]) - random.randint(0, int(char["LUCK"]))) > 0
    if success:
        item_dropped: bool = random.randint(0, 15) + int(
            int(float(char["LUCK"])) % 10000
        ) > 12
        cash_reward: int = random.randint(
            dungeon_level * 1000, dungeon_level * 5000
        ) + random.randint(100 * dungeon_level + 5, 2000 * dungeon_level + 200)
        xp_reward: int = random.randint(
            dungeon_level * 400, dungeon_level * 800
        ) + random.randint(50 * dungeon_level + 5, 200 * dungeon_level + 200)
        if char["EVOC"] == "1":
            cash_reward *= 2
            xp_reward *= 2
        if char["BLSS"] == "0":
            cash_reward *= 3
            xp_reward *= 3
        if item_dropped:
            boost: int = 0
            relic: bool = False
            if char["EVOC"] == "2":
                boost = 10000
            if char["BLSS"] == "2":
                relic = True
            item = GENERATOR.random_item(
                int(char["LUCK"]) + (dungeon_level * 100) + boost, relic
            )
        DATABASE.update_db(ctx.author.id, cash_reward, False, False)
        DATABASE.update_db(ctx.author.id, xp_reward, False, False, True)
        if item != None:
            DATABASE.add_item(ctx.author.id, item)
            color = 0xFFFFFF
            if item["rarity"] == "Relic":
                color = 0x000000
            if item["rarity"] == "Artifact":
                color = 0xFF2211
            if item["rarity"] == "Legendary":
                color = 0xAA8800
            if item["rarity"] == "Epic":
                color = 0xFF00FF
            if item["rarity"] == "Rare":
                color = 0x0000FF
            if item["rarity"] == "Uncommon":
                color = 0x00FF00
            e: discord.Embed = compose_embed(
                color,
                "Neat RPG",
                "{} got the {} drop {}!\nATK: {}\nDEF: {}\nLUCK: {}".format(
                    ctx.message.author.name,
                    item["rarity"],
                    item["name"],
                    item["ATK"],
                    item["DEF"],
                    item["LUCK"],
                ),
            )
            await ctx.send(embed=e)
        e: discord.Embed = compose_embed(
            0x00FF00,
            "Neat RPG",
            "You beat the tier {} boss {} (ATK {} - DEF {})\nand gained:\n¤{} and {}xp!".format(
                dungeon_level,
                boss["name"],
                boss["ATK"],
                boss["DEF"],
                cash_reward,
                xp_reward,
            ),
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Neat RPG",
            "The tier {} boss {} (ATK {} - DEF {})\nobliterated your feeble body!".format(
                dungeon_level, boss["name"], boss["ATK"], boss["DEF"]
            ),
        )
        await ctx.send(embed=e)


@bot.command()
async def sheet(ctx, user: discord.User = None):
    global DATABASE
    orgn_board: dict = {
        "-1": "None",
        "0": "Dragonblood",
        "1": "Bulwark",
        "2": "Gambler",
    }
    evoc_board: dict = {"-1": "None", "0": "Hellfire", "1": "Delver", "2": "Highroller"}
    blss_board: dict = {
        "-1": "None",
        "0": "Blessing of Helia",
        "1": "Blessing of Aevam",
        "2": "Blessing of Zadr",
    }
    if user == None:
        user = ctx.author
    user_data = DATABASE.get_player_data(user.id)
    char_data = DATABASE.get_character(user.id)
    weapon_data = json.loads(user_data["weapon"])
    armor_data = json.loads(user_data["armor"])
    ring_data = json.loads(user_data["ring"])
    neck_data = json.loads(user_data["neck"])
    acc_data = json.loads(user_data["accessory"])
    header: str = "[{}] {}\nOrigin: {} / Evocation: {} / Blessing: {}".format(
        user_data["level"],
        user.name,
        orgn_board[char_data["ORGN"]],
        evoc_board[char_data["EVOC"]],
        blss_board[char_data["BLSS"]],
    )
    message: str = "ATK:\t{} / DEF:\t{} / LUCK:\t{}\n\nWeapon: {}\n#{}\t(ATK {}/DEF {}/LUCK {})\n\nArmor: {}\n#{}\t(ATK {}/DEF {}/LUCK {})\n\nRing: {}\n#{}\t(ATK {}/DEF {}/LUCK {})\n\nNeck: {}\n#{}\t(ATK {}/DEF {}/LUCK {})\n\nAccessory: {}\n#{}\t(ATK {}/DEF {}/LUCK {})".format(
        user_data["rpg_attack"],
        user_data["rpg_defense"],
        user_data["rpg_luck"],
        weapon_data["name"],
        weapon_data["rarity"],
        weapon_data["ATK"],
        weapon_data["DEF"],
        weapon_data["LUCK"],
        armor_data["name"],
        armor_data["rarity"],
        armor_data["ATK"],
        armor_data["DEF"],
        armor_data["LUCK"],
        ring_data["name"],
        ring_data["rarity"],
        ring_data["ATK"],
        ring_data["DEF"],
        ring_data["LUCK"],
        neck_data["name"],
        neck_data["rarity"],
        neck_data["ATK"],
        neck_data["DEF"],
        neck_data["LUCK"],
        acc_data["name"],
        acc_data["rarity"],
        acc_data["ATK"],
        acc_data["DEF"],
        acc_data["LUCK"],
    )
    e: discord.Embed = compose_embed(0xFF00FF, header, message)
    pfp: str = user.avatar_url
    e.set_image(url=pfp)
    e.add_field(
        name="Total Stats",
        value="ATK {} - DEF {} - LUCK {}".format(
            char_data["ATK"], char_data["DEF"], char_data["LUCK"]
        ),
        inline=False,
    )
    await ctx.send(embed=e)


@bot.command()
async def origin(ctx, selection: int = -1):
    global DATABASE
    char_data = DATABASE.get_character(ctx.author.id)
    if int(char_data["LV"]) < 5:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant choose an origin until level 5!"
        )
        await ctx.send(embed=e)
        return
    if char_data["ORGN"] != "-1":
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You've already chosen your origin!"
        )
        await ctx.send(embed=e)
        return
    if selection == -1:
        e: discord.Embed = compose_embed(
            0x00FF00, "Neat RPG", "Origins, select with ?origin <id>"
        )
        e.add_field(
            name="0: Dragonblood", value="Gain extra attack with levelups", inline=False
        )
        e.add_field(
            name="1: Bulwark", value="Gain extra defense with levelups", inline=False
        )
        e.add_field(
            name="2: Gambler", value="Gain extra luck with levelups", inline=False
        )
        await ctx.send(embed=e)
        return
    if selection > 2:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "No such origin has been made yet!"
        )
        await ctx.send(embed=e)
        return
    e: discord.Embed = compose_embed(0x00FF00, "Neat RPG", "Origin chosen!")
    await ctx.send(embed=e)
    DATABASE.set_special("origin", ctx.author.id, str(selection))


@bot.command()
async def evocation(ctx, selection: int = -1):
    global DATABASE
    char_data = DATABASE.get_character(ctx.author.id)
    if int(char_data["LV"]) < 25:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant choose an evocation until level 25!"
        )
        await ctx.send(embed=e)
        return
    if char_data["EVOC"] != "-1":
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You've already chosen your evocation!"
        )
        await ctx.send(embed=e)
        return
    if selection == -1:
        e: discord.Embed = compose_embed(
            0x00FF00, "Neat RPG", "Evocations, select with ?evocation <id>"
        )
        e.add_field(
            name="0: Hellfire",
            value="Gain a boost to attack during raids",
            inline=False,
        )
        e.add_field(
            name="1: Delver", value="Get more xp and cash from dungeons", inline=False
        )
        e.add_field(
            name="2: Highroller",
            value="Get higher quality items from drops",
            inline=False,
        )
        await ctx.send(embed=e)
        return
    if selection > 2:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "No such evocation has been made yet!"
        )
        await ctx.send(embed=e)
        return
    e: discord.Embed = compose_embed(0x00FF00, "Neat RPG", "Evocation chosen!")
    await ctx.send(embed=e)
    DATABASE.set_special("evocation", ctx.author.id, str(selection))


@bot.command()
async def blessing(ctx, selection: int = -1):
    global DATABASE
    char_data = DATABASE.get_character(ctx.author.id)
    if int(char_data["LV"]) < 50:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant choose a blessing until level 50!"
        )
        await ctx.send(embed=e)
        return
    if char_data["BLSS"] != "-1":
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You've already chosen your blessing!"
        )
        await ctx.send(embed=e)
        return
    if selection == -1:
        e: discord.Embed = compose_embed(
            0x00FF00, "Neat RPG", "Blessings, select with ?blessing <id>"
        )
        e.add_field(
            name="0: Blessing of Helia",
            value="Gain far more cash and xp from dungeons and raids",
            inline=False,
        )
        e.add_field(
            name="1: Blessing of Aevam",
            value="Gain extra stats from levelups",
            inline=False,
        )
        e.add_field(
            name="2: Blessing of Zadr",
            value="Can get Relics from dungeons",
            inline=False,
        )
        await ctx.send(embed=e)
        return
    if selection > 2:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "No such blessing has been made yet!"
        )
        await ctx.send(embed=e)
        return
    e: discord.Embed = compose_embed(0x00FF00, "Neat RPG", "Blessing chosen!")
    await ctx.send(embed=e)
    DATABASE.set_special("blessing", ctx.author.id, str(selection))


@bot.command(aliases=["inv"])
async def inventory(ctx, user: discord.User = None):
    global DATABASE
    u = user
    if user == None:
        u = ctx.author
    inventory = DATABASE.get_inventory(u.id)
    pdata = DATABASE.get_player_data(u.id)
    wpn_total: int = int(json.loads(pdata["weapon"])["ATK"]) + int(
        json.loads(pdata["weapon"])["DEF"]
    ) + int(json.loads(pdata["weapon"])["LUCK"])
    arm_total: int = int(json.loads(pdata["armor"])["ATK"]) + int(
        json.loads(pdata["armor"])["DEF"]
    ) + int(json.loads(pdata["armor"])["LUCK"])
    rng_total: int = int(json.loads(pdata["ring"])["ATK"]) + int(
        json.loads(pdata["ring"])["DEF"]
    ) + int(json.loads(pdata["ring"])["LUCK"])
    nck_total: int = int(json.loads(pdata["neck"])["ATK"]) + int(
        json.loads(pdata["neck"])["DEF"]
    ) + int(json.loads(pdata["neck"])["LUCK"])
    acc_total: int = int(json.loads(pdata["accessory"])["ATK"]) + int(
        json.loads(pdata["accessory"])["DEF"]
    ) + int(json.loads(pdata["accessory"])["LUCK"])
    e: discord.Embed = compose_embed(
        0x00FF00, "Neat RPG", "{}'s inventory : [{}/16]".format(u.name, len(inventory))
    )
    i = 0
    for item in inventory:
        sign: str = "="
        unpacked = json.loads(item)
        unpacked_total: int = int(unpacked["ATK"]) + int(unpacked["DEF"]) + int(
            unpacked["LUCK"]
        )
        if unpacked["type"] == "WPN":
            if unpacked_total < wpn_total:
                sign = "-"
            if unpacked_total > wpn_total:
                sign = "+"
        if unpacked["type"] == "ARM":
            if unpacked_total < arm_total:
                sign = "-"
            if unpacked_total > arm_total:
                sign = "+"
        if unpacked["type"] == "RNG":
            if unpacked_total < rng_total:
                sign = "-"
            if unpacked_total > rng_total:
                sign = "+"
        if unpacked["type"] == "NCK":
            if unpacked_total < nck_total:
                sign = "-"
            if unpacked_total > nck_total:
                sign = "+"
        if unpacked["type"] == "ACC":
            if unpacked_total < acc_total:
                sign = "-"
            if unpacked_total > acc_total:
                sign = "+"
        e.add_field(
            name="(EquipID: {}) {}\t#{} [{}]".format(
                i, unpacked["name"], unpacked["rarity"], sign
            ),
            value="({}/{}/{})".format(
                unpacked["ATK"], unpacked["DEF"], unpacked["LUCK"]
            ),
            inline=False,
        )
        i += 1
    await ctx.send(embed=e)


@bot.command()
async def equip(ctx, equipid: int):
    global DATABASE
    max_id = len(DATABASE.get_inventory(ctx.author.id)) - 1
    if equipid > max_id or equipid < 0:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant equip an item you dont have!"
        )
        await ctx.send(embed=e)
        return
    equip_type = DATABASE.update_inventory(ctx.author.id, equipid)
    item = None
    if equip_type == "WPN":
        item = json.loads(DATABASE.get_player_data(ctx.author.id)["weapon"])["name"]
    if equip_type == "ARM":
        item = json.loads(DATABASE.get_player_data(ctx.author.id)["armor"])["name"]
    if equip_type == "RNG":
        item = json.loads(DATABASE.get_player_data(ctx.author.id)["ring"])["name"]
    if equip_type == "NCK":
        item = json.loads(DATABASE.get_player_data(ctx.author.id)["neck"])["name"]
    if equip_type == "ACC":
        item = json.loads(DATABASE.get_player_data(ctx.author.id)["accessory"])["name"]
    e: discord.Embed = compose_embed(
        0x00FF00, "Neat RPG", "Successfully equipped {}!".format(item)
    )
    await ctx.send(embed=e)


@bot.command()
async def sell(ctx, equipid: int):
    global DATABASE
    max_id = len(DATABASE.get_inventory(ctx.author.id)) - 1
    if equipid > max_id or equipid < 0:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant sell an item you dont have!"
        )
        await ctx.send(embed=e)
        return
    tmp = DATABASE.sell_item(ctx.author.id, equipid)
    print(tmp)
    item: dict = tmp[1]
    value: int = tmp[0]
    e: discord.Embed = compose_embed(
        0x00FF00,
        "Neat RPG",
        "Sold {}\t#{} for ¤{}!".format(item["name"], item["rarity"], value),
    )
    await ctx.send(embed=e)


@bot.command()
async def raid(ctx, flag=""):
    global DATABASE
    global GENERATOR
    global RAID_PLAYERS
    global RAID_BOSS
    if RAID_PLAYERS == [] and flag == "":
        RAID_BOSS = GENERATOR.generate_raid_boss()
        RAID_PLAYERS.append(ctx.author)
        e: discord.Embed = compose_embed(
            0xAA8800,
            "Raid Boss! ?raid",
            "You face the great {} {}!\n\nATK   {}\t\t\tDEF   {}".format(
                RAID_BOSS["name"],
                RAID_BOSS["suffix"],
                RAID_BOSS["ATK"],
                RAID_BOSS["DEF"],
            ),
        )
        await ctx.send(embed=e)
        return
    elif RAID_PLAYERS != [] and flag == "":
        if ctx.author in RAID_PLAYERS:
            e: discord.Embed = compose_embed(
                0xFF0000, "Raid Boss! ?raid", "You're already in the raid!"
            )
            await ctx.send(embed=e)
            return
        else:
            e: discord.Embed = compose_embed(
                0x00FF00,
                "Raid Boss! ?raid",
                "{} joined the raid!".format(ctx.author.name),
            )
            await ctx.send(embed=e)
            RAID_PLAYERS.append(ctx.author)
            return
    if flag == "start":
        combined_level: int = 0
        combined_attack: int = 0
        combined_defense: int = 0
        for player in RAID_PLAYERS:
            player_data: dict = DATABASE.get_character(player.id)
            combined_level += int(float(player_data["LV"]))
            combined_attack += int(float(player_data["ATK"]))
            combined_defense += int(float(player_data["DEF"]))
            if player_data["EVOC"] == "0":
                combined_attack += 5000
        success: bool = ((combined_level) - 200) + (
            combined_attack - int(RAID_BOSS["DEF"])
        ) - (int(RAID_BOSS["ATK"]) - combined_defense) > 0
        if success:
            Drops: discord.Embed = compose_embed(
                0x00FF00,
                "Raid Boss Defeated",
                "Your combined might of\nLevel: {} / ATK: {} / DEF: {}\n Easily overpowered the boss!".format(
                    combined_level, combined_attack, combined_defense
                ),
            )
            for player in RAID_PLAYERS:
                char = DATABASE.get_character(player.id)
                if random.randint(0, 5) > 3:
                    boost: int = 0
                    if char["EVOC"] == "2":
                        boost = 10000
                    item = GENERATOR.random_item(
                        13500 + int(float(char["LUCK"])) + boost, True
                    )
                    e: discord.Embed = compose_embed(
                        0x000000,
                        "Raid Drop",
                        "{} got the {}\t#{}!\n({}/{}/{})".format(
                            player.name,
                            item["name"],
                            item["rarity"],
                            item["ATK"],
                            item["DEF"],
                            item["LUCK"],
                        ),
                    )
                    DATABASE.add_item(player.id, item)
                    await ctx.send(embed=e)
                cash_reward: int = random.randint(50000, 250000)
                xp_reward: int = random.randint(5000, 25000)
                if char["BLSS"] == "0":
                    cash_reward *= 3
                    xp_reward *= 3
                Drops.add_field(
                    name="Raid Loot",
                    value="{} got ¤{} and {}xp for participating in the raid!".format(
                        player.name, cash_reward, xp_reward
                    ),
                    inline=False,
                )
                DATABASE.update_db(player.id, cash_reward, False, False)
                DATABASE.update_db(player.id, xp_reward, False, False, True)
                if random.randint(0, 10000) < 250:
                    mtype: str = ""
                    rng = random.randint(0, 100)
                    if rng < 100:
                        mtype = "Alpha"
                    if rng < 25:
                        mtype = "Beta"
                    if rng < 5:
                        mtype = "Gamma"
                    DATABASE.update_materials(player.id, mtype.lower(), 1)
                    materials = DATABASE.get_materials(player.id)
                    Drops.add_field(
                        name="{} was extremely lucky and got a {} material drop!".format(
                            player.name, mtype
                        ),
                        value="They now have {} {} materials!".format(
                            materials[mtype.lower()], mtype.lower()
                        ),
                        inline=False,
                    )
            await ctx.send(embed=Drops)
        else:
            e: discord.Embed = compose_embed(
                0x00FF00,
                "Raid Boss Wipe",
                "Your puny might of\nLevel: {} / ATK: {} / DEF: {}\n was easily squished by the boss!".format(
                    combined_level, combined_attack, combined_defense
                ),
            )
            await ctx.send(embed=e)
        RAID_PLAYERS = []
        RAID_BOSS = {}


@bot.command()
async def trade(ctx, user: discord.User, eid: int = -1, reid: int = -1):
    global DATABASE
    if eid == -1 or reid == -1:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You must supply equipment ids for both items!"
        )
        await ctx.send(embed=e)
        return
    if user.id == ctx.author.id:
        e: discord.Embed = compose_embed(
            0xFF0000, "Neat RPG", "You cant trade yourself!"
        )
        await ctx.send(embed=e)
        return
    success: bool = DATABASE.add_trade(ctx.author.id, user.id, eid, reid)
    if success:
        e: discord.Embed = compose_embed(
            0x00FF00, "Neat RPG", "Sent trade request to {}!".format(user.id)
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(0xFF0000, "Neat RPG", "Something went wrong!")


@bot.command()
async def trades(ctx):
    global DATABASE
    trades: list = DATABASE.get_trades(ctx.author.id)
    e: discord.Embed = compose_embed(0xFF9922, "Neat RPG", "Trade Requests")
    tid: int = 0
    idx: int = 0
    for idx in range(len(trades)):
        trade: dict = trades[idx]
        e.add_field(
            name="({}) {} {}".format(
                tid,
                trade["player_id"],
                ("<- INCOMING" if trade["type"] == "INCOMING" else "-> OUTGOING"),
            ),
            value="{}#{} ({}/{}/{})\nFOR\n{}#{} ({}/{}/{})".format(
                trade["item0"]["name"],
                trade["item0"]["rarity"],
                trade["item0"]["ATK"],
                trade["item0"]["DEF"],
                trade["item0"]["LUCK"],
                trade["item1"]["name"],
                trade["item1"]["rarity"],
                trade["item1"]["ATK"],
                trade["item1"]["DEF"],
                trade["item1"]["LUCK"],
            ),
            inline=False,
        )
    await ctx.send(embed=e)


@bot.command()
async def cancel(ctx, tid: int):
    global DATABASE
    trades = DATABASE.get_trades(ctx.author.id)
    if tid >= 0 and tid < len(trades):
        success: bool = DATABASE.resolve_trade(ctx.author.id, tid, False)
        if success:
            e: discord.Embed = compose_embed(
                0x00FF00, "Neat RPG", "Cancelled trade #{}!".format(tid)
            )
            await ctx.send(embed=e)
        else:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Neat RPG",
                "Something went wrong trying to accept that trade! Are you sure its outgoing?",
            )
            await ctx.send(embed=e)
    else:
        await ctx.send(
            embed=compose_embed(
                0xFF0000, "Neat RPG", "You cant resolve a nonexistant trade!"
            )
        )


@bot.command()
async def accept(ctx, tid: int):
    global DATABASE
    trades = DATABASE.get_trades(ctx.author.id)
    if tid >= 0 and tid < len(trades):
        success: bool = DATABASE.resolve_trade(ctx.author.id, tid, True)
        if success:
            e: discord.Embed = compose_embed(
                0x00FF00, "Neat RPG", "Accepted trade #{}!".format(tid)
            )
            await ctx.send(embed=e)
        else:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Neat RPG",
                "Something went wrong trying to accept that trade! Are you sure its incoming?",
            )
            await ctx.send(embed=e)
    else:
        await ctx.send(
            embed=compose_embed(
                0xFF0000, "Neat RPG", "You cant resolve a nonexistant trade!"
            )
        )


@bot.command()
async def decline(ctx, tid: int):
    global DATABASE
    trades = DATABASE.get_trades(ctx.author.id)
    if tid >= 0 and tid < len(trades):
        success: bool = DATABASE.resolve_trade(ctx.author.id, tid, False)
        if success:
            e: discord.Embed = compose_embed(
                0x00FF00, "Neat RPG", "Declined trade #{}!".format(tid)
            )
            await ctx.send(embed=e)
        else:
            e: discord.Embed = compose_embed(
                0xFF0000,
                "Neat RPG",
                "Something went wrong trying to accept that trade!",
            )
            await ctx.send(embed=e)
    else:
        await ctx.send(
            embed=compose_embed(
                0xFF0000, "Neat RPG", "You cant resolve a nonexistant trade!"
            )
        )


@bot.command()
async def forge(ctx, mtype: str = ""):
    global DATABASE
    global GENERATOR
    global MATERIALS_PER_ITEM
    author = ctx.author
    if mtype not in ("alpha", "beta", "gamma"):
        e: discord.Embed = compose_embed(0xFF0000, "Neat RPG", "Illegal material type!")
        await ctx.send(embed=e)
        return
    success: bool = DATABASE.update_materials(
        author.id, mtype, MATERIALS_PER_ITEM, True
    )
    if not success:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "Neat RPG",
            "You do not have enough materials to make an item of this quality",
        )
        await ctx.send(embed=e)
        return
    item = GENERATOR.forge_item(mtype)
    DATABASE.add_item(author.id, item)
    e: discord.Embed = compose_embed(
        0x00FF00,
        "Neat RPG",
        "You successfully forged the item {} - #{} ({})".format(
            item["name"], item["rarity"], item["type"]
        ),
    )
    await ctx.send(embed=e)
    return


@bot.command()
async def materials(ctx, user: discord.User = None):
    global DATABASE
    if user == None:
        user = ctx.author
    materials = DATABASE.get_materials(user.id)
    e: discord.Embed = compose_embed(
        0xFF00FF, "Neat RPG", "{}'s materials".format(user.name)
    )
    e.add_field(name="α materials", value="{}".format(materials["alpha"]), inline=False)
    e.add_field(name="β materials", value="{}".format(materials["beta"]), inline=False)
    e.add_field(name="γ materials", value="{}".format(materials["gamma"]), inline=False)
    await ctx.send(embed=e)


# Admin commands


@bot.command()
async def forcesave(ctx):
    global DATABASE
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        e: discord.Embed = compose_embed(
            0x00FF00, "ADMIN COMMAND", "Saving internal state to DB ..."
        )
        msg = await ctx.send(embed=e)
        DATABASE.push()
        e = compose_embed(0x00FF00, "ADMIN COMMAND", "Saved!")
        await msg.edit(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "ADMIN COMMAND",
            "I'm sorry, but you dont look like an admin to me",
        )
        await ctx.send(embed=e)


@bot.command()
async def giveitem(
    ctx, user: discord.User, name: str, itemtype: str, atk: int, defn: int, luck: int
):
    global DATABASE
    global GENERATOR
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        e: discord.Embed = compose_embed(0x00FF00, "ADMIN COMMAND", "Creating item ...")
        msg = await ctx.send(embed=e)
        item = GENERATOR.make_unique_item(name, itemtype, atk, defn, luck)
        DATABASE.add_item(user.id, item)
        e = compose_embed(
            0x00FF00,
            "ADMIN COMMAND",
            "Added {} to {}'s inventory!".format(item["name"], user.name),
        )
        await msg.edit(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "ADMIN COMMAND",
            "I'm sorry, but you dont look like an admin to me",
        )
        await ctx.send(embed=e)


@bot.command(pass_context=True)
async def mute(ctx, user: discord.Member, time: int):
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        role = discord.utils.get(user.guild.roles, name="Muted")
        await user.add_roles(role)
        e: discord.Embed = compose_embed(
            0x00FF00, "ADMIN COMMAND", "Muted {} for {} seconds".format(user.name, time)
        )
        await ctx.send(embed=e)
        await asyncio.sleep(float(time))
        await user.remove_roles(role)
        e = compose_embed(
            0xFF0000, "ADMIN COMMAND", "User {} has been unmuted.".format(user.name)
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "ADMIN COMMAND",
            "I'm sorry, but you dont look like an admin to me",
        )
        await ctx.send(embed=e)


@bot.command()
async def kick(ctx, user: discord.Member, *reason):
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        await ctx.guild.kick(user, reason=" ".join(reason))
        e: discord.Embed = compose_embed(
            0x00FF00,
            "ADMIN COMMAND",
            "Kicked {} for {}".format(user.name, " ".join(reason)),
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "ADMIN COMMAND",
            "I'm sorry, but you dont look like an admin to me",
        )
        await ctx.send(embed=e)


@bot.command()
async def ban(ctx, user: discord.Member, *reason):
    is_admin: bool = ctx.author.top_role.permissions.administrator
    if is_admin:
        await ctx.guild.ban(user, reason=" ".join(reason))
        e: discord.Embed = compose_embed(
            0x00FF00,
            "ADMIN COMMAND",
            "Banned {} for {}".format(user.name, " ".join(reason)),
        )
        await ctx.send(embed=e)
    else:
        e: discord.Embed = compose_embed(
            0xFF0000,
            "ADMIN COMMAND",
            "I'm sorry, but you dont look like an admin to me",
        )
        await ctx.send(embed=e)


bot.run(
    TOKEN
)  # E O F ==========================================================================================================
