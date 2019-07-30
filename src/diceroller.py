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
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.voice_client import VoiceClient
from colorama import init

init()
from colorama import Fore as F
from colorama import Style as S
from colorama import Back as B
from datetime import datetime
import random

# Logging
import logging
from cn_globals import *
import cndb

DATABASE = cndb.CNDatabase()

logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)
# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix="?", case_insensitive=True)

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
    msg = discord.Embed(title="CN Diceroller", description="", color=color)
    msg.add_field(name=name, value=content, inline=False)
    return msg


# Bot events
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


async def push_database_task():
    global DATABASE
    global DB_PUSH_TIMEOUT

    while True:
        DATABASE.push()
        await asyncio.sleep(DB_PUSH_TIMEOUT)


@bot.event
async def on_ready():
    global AUTHOR
    global DATABASE

    DATABASE.pull()
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
    print("Bot connected\t\t{} [V:1.0]\t\t\t\t".format(date_time))
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
    # Necessary variables for logging, events, etc.
    # Also cleaning of message contents for a better reading experience
    rnd = random.randint(0, 5000)
    guild = message.guild
    author = message.author
    channel = message.channel
    content = message.content
    content = content.replace("*", "")
    content = content.replace("`", "")
    content = content.replace("_", "")
    content = content.replace("~", "")
    # We dont want to give bots xp
    if not author.bot:
        msg = DATABASE.register(author)
        if msg != None:
            await message.channel.send(
                "```User {} has been registered!```".format(author.name)
            )
        xp = random.randint(10, 25)
        debug_console_log("on_message", author, "awarded {}xp for messsage".format(xp))
        xp_return: int = DATABASE.update_db(
            author.id, xp, False, False, True
        )  # -1 if not registered
        if xp_return == -1:
            await message.channel.send(
                "```User {} has been registered!```".format(author.name)
            )
    # Random cash events
    if rnd < 100 and rnd > 10 and not RANDOM_EVENT_CURRENTLY:
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
    elif rnd < 10 and not RANDOM_EVENT_CURRENTLY:
        RANDOM_EVENT_CURRENTLY = True
        coinflip: int = random.randint(0, 100)
        if coinflip < 50:
            CRATE_GIVES_XP = True
        crate_rarity_roll: int = random.randint(0, 100)
        crate_rarity: str = ""
        if crate_rarity_roll < 75:
            crate_rarity = "Common"
        if crate_rarity_roll < 50:
            crate_rarity = "Uncommon"
        if crate_rarity_roll < 25:
            crate_rarity = "Rare"
        if crate_rarity_roll < 10:
            crate_rarity = "Epic"
        CRATE_REWARD_AMOUNT = (100 - crate_rarity_roll) * 10
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
            + "[@{}/USER]\t(#{})\t({}) {}: {}".format(
                guild.name, channel.name, author.id, author.name, content
            )
        )
    if author.bot and not FILTER_BOTS:
        print(
            S.BRIGHT
            + F.MAGENTA
            + "[@{}/BOT]\t(#{})\t{}: {}".format(
                guild.name, channel.name, author.name, content
            )
        )
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
    msg = discord.Embed(title="CN Diceroller", description="", color=0xFF00FF)
    msg.add_field(
        name="?help",
        value="Displays this message.\nAlias=[h, info, commands, c]",
        inline=False,
    )
    msg.add_field(
        name="?roll <dice><sides>[mod]",
        value="Rolls some variable-sided dice and prints the result.\nAlias=[r]",
        inline=False,
    )
    msg.add_field(name="?rigg", value="Nice try", inline=False)
    msg.add_field(name="?rigged", value="How dare you!", inline=False)
    msg.add_field(
        name="?gamble <bet>",
        value="Dicegame, betting ¤<bet> against a 100-sided roll, over 55 is a win.\nAlias=[55x2, g, bet]",
        inline=False,
    )
    msg.add_field(
        name="?bal",
        value="Shows you how much money you have.\nAlias=[balance, eco, money]",
        inline=False,
    )
    msg.add_field(
        name="?daily", value="Claim a daily cash bonus.\nAlias=[d]", inline=False
    )
    msg.add_field(
        name="?order <drink>",
        value="Buy a drink! userexperiencenotguaranteed",
        inline=False,
    )
    msg.add_field(
        name="?pay <user> <amount>",
        value="Send someone your hard-earned money.\nAlias=[give]",
        inline=False,
    )
    msg.add_field(
        name="?insult <name>", value="Generate an insult aimed at someone", inline=False
    )
    msg.add_field(
        name="?compliment <name>",
        value="Generate a compliment aimed at someone",
        inline=False,
    )
    msg.add_field(
        name="?level <user:optional>",
        value="Show someone's level and xp count",
        inline=False,
    )
    msg.add_field(name="?adminhelp", value="Show admin-only commands", inline=False)
    await ctx.send(embed=msg)


@bot.command()
async def adminhelp(ctx):
    """
	adminhelp: 	
			displays a help message for administrators
	Requires:
			Nothing
	"""
    debug_console_log("adminhelp", ctx.message.author)
    msg = discord.Embed(title="CN Adminpanel", description="", color=0xFF0000)
    msg.add_field(name="?debug", value="(ADMIN) DB debug command", inline=False)
    msg.add_field(
        name="?update <@user> <amount>",
        value="(ADMIN) Give a user the provided amount",
        inline=False,
    )
    msg.add_field(
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
    await ctx.send(embed=msg)
    await ctx.send(embed=filters)


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
        tmp -= 500 + (250 * level)  # To make later levels a bit more challenging
    e = compose_embed(
        0xFFFFFF,
        "{}, Level {}".format(target.name, level),
        "{} has {}xp".format(target.name, target_xp),
    )
    await ctx.send(embed=e)


@bot.command(aliases=["d"])
async def daily(ctx):
    global DATABASE
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
        i = 0
        for i in range(dice):
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


# Show a user their balance
@bot.command(aliases=["money", "balance", "eco"])
async def bal(ctx):
    """
	Bal: 	
			responds with the users balance.
	Requires:
			user must be registered
	"""
    global DATABASE

    author = ctx.message.author
    balance = DATABASE.update_db(author.id, 0, False, False)
    e = compose_embed(0x00FF00, "{} has ¤{}".format(author.name, balance), "ID: {}".format(author.id))
    await ctx.send(embed=e)


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
        e = compose_embed(0xFF0000, "Giving yourself an allowance is weird, man", "C'mon, you're better than this")
        await ctx.send(embed=e)
        return
    msg = DATABASE.register(user_to)
    if amount < 0:
        e = compose_embed(0xFF0000, "Theft is illegal", "The authorities have been alerted.")
        await ctx.send(embed=e)
        print("=================================================")
        print("{} Attempted to steal from {}".format(user_from.name, user_to.name))
        print("=================================================")
        return
    if user_to.bot:
        e = compose_embed(0xFF0000, "Bot's dont have money, silly", "C'mon")
        await ctx.send(embed=e)
        return
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
    drinks: list = ["beer", "cider", "wine", "rum", "vodka", "whiskey"]
    prices: list = [5, 5, 10, 12, 12, 15]
    if drink == "empty":
        e = discord.Embed(title="CN Diceroller", description="", color=0x662200)
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
            update_success: int = DATABASE.update_db(author.id, price, True)
            if update_success != -1:
                e = compose_embed(
                    0xFFFFFF,
                    "You buy a class of {}".format(drink.lower()),
                    "You feel scammed",
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
        "Your parents love you, and even if they dont, I sure do ",
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


bot.run(TOKEN)
