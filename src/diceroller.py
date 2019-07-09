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

import discord
import random
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.voice_client import VoiceClient
from colorama import init
init()
from colorama import Fore as F
from colorama import Style as S
from colorama import Back as B

from datetime import datetime
# Logging
import logging
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)

# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix='?', case_insensitive=True)

# I'm really sorry but globals are really the easiest way of handling this
RIGGED 					= False
DB 						= "DB/database.cndb"
DBTMP 					= "DB/tmp.cncrypt"
DB_LEVEL 				= "DB/leveldatabase.cndb"
RANDOM_EVENT_CURRENTLY 	= False
RANDOM_EVENT_AMOUNT 	= 0
FILTER_USERS 			= False
FILTER_BOTS  			= False
FILTER_LOGS  			= False

# OC dont steal
TOKEN = ""
with open("enc/token.cncrypt", "r+") as tfile:
	TOKEN = tfile.readline()

# Helper function. Sends a debug message to the console. Used to standardize input and make changes easier, and debugs clearer.
def debug_console_log(source: str, author: discord.User, msg: str = "") -> None:
	global RIGGED
	global FILTER_LOGS

	is_admin: bool = author.top_role.permissions.administrator
	if not FILTER_LOGS:
		print(S.BRIGHT + F.YELLOW + "[DEBUG|LOG]\t#{}: ({}) {}: {}\n[DEBUG|LOG]\tRigged: {} - Admin: {}".format(source, author.id, author.name, msg, RIGGED, is_admin))


# Helper function. Registers a user to the bot DB
def register(user: discord.User):
	global DB
	global DB_LEVEL
	line: str = "0000000000000"
	with open(DB, "r+") as db: # ah shit, here we go again
		while line != "":
			try:
				line = db.readline()		# check users
				if str(user.id) in line:
					split: list = line.split("/")
					return None
			except StopIteration:			# register them if they're not in the DB
				debug_console_log("register", user, "Error: Hit EOF before end of loop")
		db.write(str(user.id) + "/1000\n")
	line = "0000000000000"
	with open(DB_LEVEL, "r+") as ldb: # ah shit, here we go again
		while line != "":
			try:
				line = ldb.readline()		# check users
				if str(user.id) in line:
					split: list = line.split("/")
					return None
			except StopIteration:			# register them if they're not in the DB
				debug_console_log("register", user, "Error: Hit EOF before end of loop")
		ldb.write(str(user.id) + "/0\n")
	return ("```User {} has been registered!```".format(user.name))


# Helper function. Does all of the interfacing between the bot and the DB
def update_db(userid, amount: int, sub: bool, isBet: bool = True) -> bool:
	global DB
	global DBTMP

	line = "0000000000"
	# HERE WE GOOO
	with open(DB, "r+") as db:
		while line != "":
			try: # Use exceptions to find the EOF
				line = db.readline()
				if str(userid) in line: # If we found the user
					split: list = line.split("/") # Get the balance and id seperately
					bal: str = split[1] 
					if int(bal) < amount and isBet: # cant bet more than you have
						return False
					if sub:
						bal = str(int(bal) - amount)
					else:
						bal = str(int(bal) + amount)
					newline = str(userid) + "/" + str(bal) # make the new db entry
					tmpdata = "0000000"
					with open(DBTMP, "w") as clear: # clear the tmp file, just in case
						clear.write("")
					with open(DBTMP, "r+") as tmp:  # transfer all db info to temporary storage
						with open(DB, "r+") as db:
							while tmpdata != "":
								dbline = db.readline()
								tmpdata = dbline
								if dbline == line:			# write the new line instead of the old one
									tmp.write(newline+"\n")
								else:
									tmp.write(dbline+"\n")
					tmpdata = "0000000"
					with open(DB, "w") as clear:		# clear the db
						clear.write("")
					with open(DB, "r+") as db:			# rewrite the db for future use
						with open(DBTMP, "r+") as tmp:
							while tmpdata != "":
								tmpdata = tmp.readline()
								if(tmpdata != "\n"): db.write(tmpdata)
					with open(DBTMP, "w") as clear:	# clear tmp to have it ready for the next pass
						clear.write("")
					return True
			except StopIteration:
				return False

# Helper function. Does all of the interfacing between the bot and the DB
# Returns -1 if not registered, then registers.
def update_level_db(user, amount: int) -> int:
	global DB_LEVEL
	global DBTMP
	xp_after_update: int = 0
	userid = user.id
	line = "0000000000"
	# HERE WE GOOO
	with open(DB_LEVEL, "r+") as db:
		while line != "":
			try: # Use exceptions to find the EOF
				line = db.readline()
				if str(userid) in line: # If we found the user
					split: list = line.split("/") # Get the balance and id seperately
					xp: str = split[1]
					xp_after_update = int(xp) + amount
					newline = str(userid) + "/" + str(xp_after_update) # make the new db entry
					tmpdata = "0000000"
					with open(DBTMP, "w") as clear: # clear the tmp file, just in case
						clear.write("")
					with open(DBTMP, "r+") as tmp:  # transfer all db info to temporary storage
						with open(DB_LEVEL, "r+") as db:
							while tmpdata != "":
								dbline = db.readline()
								tmpdata = dbline
								if dbline == line:			# write the new line instead of the old one
									tmp.write(newline+"\n")
								else:
									tmp.write(dbline+"\n")
					tmpdata = "0000000"
					with open(DB_LEVEL, "w") as clear:		# clear the db
						clear.write("")
					with open(DB_LEVEL, "r+") as db:			# rewrite the db for future use
						with open(DBTMP, "r+") as tmp:
							while tmpdata != "":
								tmpdata = tmp.readline()
								if(tmpdata != "\n"): db.write(tmpdata)
					with open(DBTMP, "w") as clear:	# clear tmp to have it ready for the next pass
						clear.write("")
					return xp_after_update
			except StopIteration:
				register(user)
				return -1

# Bot events
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.event
async def on_ready():
	now = datetime.now()
	server_count: int = len(bot.guilds)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{} servers | ?help".format(server_count)))
	date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
	if not hasattr(bot, 'appinfo'):
		bot.appinfo = await bot.application_info()
	print(S.BRIGHT + B.WHITE + F.BLUE + "--------------------------------------------------------------------------------")
	print("Bot connected\t\t{} [V:BETA]\t\t\t\t".format(date_time))
	print("ID:\t\t\t{}\t\t\t\t\t\nName:\t\t\t{}\t\t\t\t\t\nOwner:\t\t\t{}\t\t\t\t\t\t\nAuthor:\t\t\tZet#1024 (github.com/ZexZee)\t\t\t\t".format(
																											bot.appinfo.id, bot.appinfo.name, bot.appinfo.owner))
	print("--------------------------------------------------------------------------------" + S.RESET_ALL)


@bot.event
async def on_message(message):
	global RANDOM_EVENT_CURRENTLY
	global RANDOM_EVENT_AMOUNT
	global FILTER_LOGS
	global FILTER_BOTS
	global FILTER_USERS

	rnd = random.randint(0, 5000)
	guild = message.guild
	author = message.author
	channel = message.channel
	content = message.content
	content = content.replace("*", "")
	content = content.replace("`", "")
	if not author.bot:
		xp = random.randint(10, 25)
		debug_console_log("on_message", author, "awarded {}xp for messsage".format(xp))
		xp_return: int = update_level_db(author, xp)
		if xp_return == -1:
			await message.channel.send("```User {} has been registered!```".format(author.name))
	if rnd < 100 and not RANDOM_EVENT_CURRENTLY:
		RANDOM_EVENT_CURRENTLY = True
		RANDOM_EVENT_AMOUNT = random.randint(100, 10000)
		print(S.BRIGHT + F.YELLOW + "[DEBUG|LOG]\tRandom event for ¤{} created".format(RANDOM_EVENT_AMOUNT))
		await message.channel.send("¤{} just materialized out of nothing, get it with `?grab`!".format(RANDOM_EVENT_AMOUNT))
	if not author.bot and not FILTER_USERS:
		print(S.BRIGHT + F.CYAN + "[@{}\tUSER]\t(#{})\t({}) {}: {}".format(guild.name, channel.name, author.id, author.name, content))
	if author.bot and not FILTER_BOTS:
		print(S.BRIGHT + F.MAGENTA + "[@{}\tBOT]\t(#{})\t{}: {}".format(guild.name, channel.name, author.name, content))
	await bot.process_commands(message)


bot.remove_command('help')
# Help messages
@bot.command(aliases=['h', 'info', 'commands', 'c'])
async def help(ctx):
	"""
	help: 	
			displays a help message
	Requires:
			Nothing
	"""
	debug_console_log("help", ctx.message.author)
	msg = discord.Embed(title="CN Diceroller", 			description="", 																					color=0xff00ff)
	msg.add_field(		name="?help", 					value="Displays this message.\nAlias=[h, info, commands, c]", 										inline=False)
	msg.add_field(		name="?roll <dice> <sides>", 	value="Rolls some variable-sided dice and prints the result.\nAlias=[r]", 							inline=False)
	msg.add_field(		name="?rigg", 					value="Nice try", 																					inline=False)
	msg.add_field(		name="?rigged", 				value="How dare you!", 																				inline=False)
	msg.add_field(		name="?gamble <bet>", 			value="Dicegame, betting ¤<bet> against a 100-sided roll, over 55 is a win.\nAlias=[55x2, g, bet]", inline=False)
	msg.add_field(		name="?bal", 					value="Shows you how much money you have.\nAlias=[balance, eco, money]", 							inline=False)
	msg.add_field(		name="?order <drink>", 			value="Buy a drink! userexperiencenotguaranteed", 													inline=False)
	msg.add_field(		name="?pay <user> <amount>", 	value="Send someone your hard-earned money.\nAlias=[give]", 										inline=False)
	msg.add_field(		name="?insult <name>", 			value="Generate an insult aimed at someone", 														inline=False)
	msg.add_field(		name="?compliment <name>", 		value="Generate a compliment aimed at someone", 													inline=False)
	msg.add_field(		name="?grab", 					value="Used to grab a randomly spawned event amount", 												inline=False)
	msg.add_field(		name="?level <user:optional>", 	value="Show someone's level and xp count", 															inline=False)
	msg.add_field(		name="?adminhelp", 				value="Show admin-only commands", 																	inline=False)
	await ctx.send(		embed=msg)


@bot.command()
async def adminhelp(ctx):
	"""
	adminhelp: 	
			displays a help message for administrators
	Requires:
			Nothing
	"""
	debug_console_log("adminhelp", ctx.message.author)
	msg = discord.Embed(	title="CN Adminpanel", 				description="", 										color=0xff0000)
	msg.add_field(			name="?debug", 						value="(ADMIN) DB debug command", 						inline=False)
	msg.add_field(			name="?update <@user> <amount>", 	value="(ADMIN) Give a user the provided amount", 		inline=False)
	msg.add_field(			name="?raffle <prizeamount>", 		value="(ADMIN) Gives a random registered user a prize", inline=False)
	msg.add_field(			name="?filter <value>", 			value="(ADMIN) Filters console output.", 				inline=False)
	filters = discord.Embed(title="CN Filters", 				description="A list of filters for the admin console", 	color=0x0000ff)
	filters.add_field(		name="users", 						value="Toggles user messages on/off", 					inline=False)
	filters.add_field(		name="bots", 						value="Toggles bot messages on/off", 					inline=False)
	filters.add_field(		name="debug", 						value="Toggles debug messages on/off", 					inline=False)
	filters.add_field(		name="all", 						value="Toggles all messages on", 						inline=False)
	filters.add_field(		name="none", 						value="Toggles all messages off", 						inline=False)
	await ctx.send(			embed=msg)
	await ctx.send(			embed=filters)


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
			FILTER_USERS	= not FILTER_USERS
			await ctx.send("```Filter switched! Showing users : {}```".format(not FILTER_USERS))
		elif f == "bots":
			FILTER_BOTS 	= not FILTER_BOTS
			await ctx.send("```Filter switched! Showing bots : {}```".format(not FILTER_BOTS))
		elif f == "debug":
			FILTER_LOGS 	= not FILTER_LOGS
			await ctx.send("```Filter switched! Showing logs : {}```".format(not FILTER_LOGS))
		elif f == "all":
			FILTER_USERS 	= False
			FILTER_BOTS 	= False
			FILTER_LOGS 	= False
			await ctx.send("```Filters switched! Now showing all messages```")
		elif f == "none":
			FILTER_USERS 	= True
			FILTER_BOTS 	= True
			FILTER_LOGS 	= True
			await ctx.send("```Filters switched! Now showing no messages```")
		else:
			await ctx.send("```Malformed argument - No such filter```")


@bot.command()
async def grab(ctx):
	global RANDOM_EVENT_AMOUNT
	global RANDOM_EVENT_CURRENTLY

	author = ctx.message.author
	debug_console_log("grab", author)
	if RANDOM_EVENT_CURRENTLY:
		update_success: bool = update_db(author.id, RANDOM_EVENT_AMOUNT, False, False)
		if update_success:
			RANDOM_EVENT_CURRENTLY = False
			await ctx.send("```Congrats to {}, for grabbing that free ¤{}```".format(author.name, RANDOM_EVENT_AMOUNT))
			RANDOM_EVENT_AMOUNT = 0
		else:
			await ctx.send("```Error updating DB```")
	else:
		await ctx.send("```Theres no random event, currently```")


@bot.command()
async def level(ctx, user: discord.User = None):
	target = user
	author = ctx.message.author
	if target == None:
		target = author
	else:
		msg = register(target)
		if msg != None:
			await ctx.send(msg)
	debug_console_log("level", author, "targets other: {} | target: {}".format((target != None), target))
	target_xp = update_level_db(target, 0)
	tmp = target_xp
	level = 0
	while tmp > 0:
		level += 1
		tmp -= (500 + (250 * level)) # To make later levels a bit more challenging
	await ctx.send("```User {} is level {} with {}xp```".format(target.name, level, target_xp))


# Roll a dice with a variable amount of sides
@bot.command(aliases=['r'])
async def roll(ctx, dice: int = 1, sides: int = 6):
	"""
	Roll: 	
			performs a riggable roll, printing the result in the chat used, utilizing the sides and dicecount provided.
	Requires:
			Nothing
	"""
	global RIGGED

	author = ctx.message.author
	debug_console_log("roll", author)
	if dice == 1:
		if sides <= 1:
			# Someone will definitely attempt to roll a "0 sided die" and thats dumb
			await ctx.send("```Are you braindead? Do you not know how dice work?```")
			return
		roll = random.randint(1, sides)
		if RIGGED:
			# If you wanna rigg a throw, make sure it always gets the max
			await ctx.send('```Rolled a {} - {}d{}```'.format(sides, dice, sides))
			RIGGED = False
			print("Rig successfull, returning to standard, boring \"FAIR\" mode.")
		else:
			await ctx.send("```Rolled a {} - {}d{}```".format(roll, dice, sides))
	else:
		dicerolls: list = []
		i = 0
		for i in range(dice):
			if RIGGED:
				if sides > 2:
					dicerolls.append(random.randint(sides - 1, sides))
				else:
					dicerolls.append(sides)
			else:
				dicerolls.append(random.randint(1, sides))
		RIGGED = False
		await ctx.send("```Rolled: {} - {}d{}```".format(dicerolls, dice, sides))


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
		await ctx.send("```I'm deeply offended that you'd assume I have such functionality```")


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
	await ctx.send("```How DARE you accuse me of rigging something as holy as a dice throw you degenerate manatee!```")


# Dice game, most of the code is DB stuff
@bot.command(aliases=['55x2', 'g', 'bet'])
async def gamble(ctx, bet: int = 0):
	"""
	gamble: 	
			rolls a 100-sided die with a provided bet, and pays out double if above 55.
	Requires:
			User must be registered and have a sufficient balance to play the game
	"""
	global RIGGED

	author = ctx.message.author
	if bet <= 0:
		await ctx.send("```You need to actually supply a bet, y'know```")
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
	update_success: bool = False
	debug_console_log("gamble", author, "¤{} | Won: {}".format(bet, roll > 55))
	if roll <= 55:
		update_success = update_db(author.id, int(bet), True)
		if update_success:
			await ctx.send("```I'm sorry, you just lost ¤{} with a roll of {}```".format(bet, roll))
			return
		else:
			await ctx.send("```You do not have enough money to place that bet```")
			return
	else:
		update_success = update_db(author.id, int(bet), False)
		if update_success:
			await ctx.send("```Congrats, you just won ¤{} with a roll of {}```".format(bet, roll))
			return
		else:
			await ctx.send("```You do not have enough money to place that bet```")
			return


# Show a user their balance
@bot.command(aliases=['money', 'balance', 'eco'])
async def bal(ctx):
	"""
	Bal: 	
			responds with the users balance.
	Requires:
			user must be registered
	"""
	global DB

	author = ctx.message.author
	line: str = "0000000000000"
	with open(DB, "r+") as db: # getting really tired of file i/o
		while line != "":
			try:
				line = db.readline()
				if str(author.id) in line:
					split: list = line.split("/") # if we find them, respond with their balance and cease
					bal: str = split[1].rstrip()
					debug_console_log("bal", author, "Has: ¤{}".format(bal))
					await ctx.send("```{} has ¤{}```".format(author.name, bal))
					return
			except StopIteration:
				debug_console_log("bal", author, "Error: User not found")
				await ctx.send("```Error retrieving balance```")


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
	global DB
	global DB_LEVEL
	author = ctx.message.author
	is_admin: bool = author.top_role.permissions.administrator
	debug_console_log("debug", author)
	# I really dont want people to spam debug info
	if is_admin:
		registered_users: int = 0
		total_balance: int = 0
		total_xp: int = 0
		line: str = "0000000000000"
		lv_line: str = "0000000000000"
		print(S.BRIGHT + B.WHITE + F.BLUE)
		with open(DB_LEVEL, "r+") as ldb:
			with open(DB, "r+") as db: # getting really tired of file i/o
				while line != "":
					try:
						line = db.readline() # calculate totals and print individual info
						lv_line = ldb.readline()
						split: list = line.split("/")
						lv_split: list = lv_line.split("/")
						if len(split) >1 and len(lv_split) >1:	 # ghost users are a thing
							bal: str = split[1]
							xp: str = lv_split[1]
							registered_users += 1
							total_balance += int(bal)
							total_xp += int(xp)
							print("User: {} - Balance: ¤{} - XP: {}".format(split[0].rstrip(), bal.rstrip(), xp.rstrip()))
					except StopIteration:
						debug_console_log("debug", author, "Error: Hit EOF before end of loop")
						break
		print("Total users: {}\t\tTotal balance: ¤{}\t\tTotal xp: {}".format(registered_users, total_balance, total_xp))
		await ctx.send("```Info sent to the console! Current user count: {}, total balance: ¤{}, total xp: {}```".format(registered_users, total_balance, total_xp))
	else:
		await ctx.send("```Nice try, pleb```")
	print(S.RESET_ALL)


# Change someones balance
@bot.command()
async def update(ctx, user: discord.User, amount: int):
	"""
	Update: 	
			gives the specified user <amount> extra ¤.
	Requires:
			Administrator permission, for what i hope is an obvious reason. User must also be registered
	"""
	author = ctx.message.author
	is_admin: bool = author.top_role.permissions.administrator
	debug_console_log("update", author, "Target: ({}) {}, update amount: ¤{}".format(user.id, user.name, amount))
	# I really dont want normal people to do this
	if is_admin:
		update_success: bool = update_db(user.id, amount, False, False)
		if update_success:
			await ctx.send("```Added ¤{} to {}'s balance```".format(amount, user.name))
			return
		else:
			await ctx.send("```I cant update a nonexistant balance! (?register)```")
			return
	else:
		await ctx.send("```Thats a no from me dawg```")


@bot.command()
async def raffle(ctx, prize: int):
	"""
	Raffle:
			give a prize amount to a random registered user.
	Requires:
			Administrator permission, to avoid effectively destroying the economy. Users must be registered, prize amount must be given.
	"""
	global DB
	global RIGGED

	author = ctx.message.author
	is_admin: bool = author.top_role.permissions.administrator
	winner_id = ""
	debug_console_log("raffle", author)
	if is_admin:
		user_ids: list = []
		line: str = "000000000"
		if RIGGED:
			winner_id = str(author.id)
			RIGGED = False
		else:
			with open(DB, "r+") as db:
				while line != "":
					try:
						line = db.readline()
						split = line.split("/")
						current_id = split[0]
						if current_id != "": user_ids.append(current_id)
					except StopIteration:
						debug_console_log("raffle", author, "Error: Hit EOF before end of loop")
			roll = random.randint(0, len(user_ids) -1)
			winner_id = user_ids[roll]
		update_success: bool = update_db(winner_id, prize, False, False)
		if update_success:
			await ctx.send("**Congratulations, <@{}>! You just won ¤{} in the raffle hosted by {}**".format(winner_id, prize, author.name))
			return
		else:
			await ctx.send("```Error finding winner of raffle!```")
			return
	

@bot.command(aliases=['give'])
async def pay(ctx, user: discord.User, amount: int):
	"""
	Pay:
			Give another user money from your own balance.
	Requires:
			The user to pay, the amount to pay, and a balance that covers the amount.
	"""
	user_from = ctx.message.author
	user_to   = user
	msg = register(user_to)
	if msg != None:
		await ctx.send(msg)
	debug_console_log("pay", user_from, "Target: ({}) {}, amount: ¤{}".format(user_to.id, user_to.name, amount))
	update_success_deduct: bool = update_db(user_from.id, amount, True)
	if update_success_deduct:
		update_success_increase: bool = update_db(user_to.id, amount, False, False)
		if update_success_increase:
			await ctx.send("```{} successfully sent ¤{} to {}!```".format(user_from.name, amount, user_to.name))
			return
		else:
			update_success_reset: bool = update_db(user_from.id, amount, False, False)
			if update_success_reset:
				await ctx.send("```Error during transfer, you have not been charged```")
				return
			else:
				await ctx.send("```Error during transfer, you HAVE been charged, please contact an admin```")
				return
	else:
		await ctx.send("```Error withdrawing funds. Do you have enough?```")
		return


@bot.command()
async def order(ctx, drink: str = "empty"):
	"""
	Order:
			Order a functionally non-existant drink with no effects.
	Requires:
			Enough money to buy the required drink, aswell as the drink to buy.
	"""
	author = ctx.message.author
	debug_console_log("order", author, "Drink: {}".format(drink))
	# Dict would be preferable but I'm tired and just want to iterate
	drinks: list = [
					"beer", 
					"cider", 
					"wine", 
					"rum", 
					"vodka", 
					"whiskey"
	]
	prices: list = [5, 5, 10, 12, 12, 15]
	if drink == "empty":
		await ctx.send("What can I getcha?")
		await ctx.send("I currently have ...")
		i = 0
		while i < (len(drinks)):
			await ctx.send("{} for ¤{}".format(drinks[i], prices[i]))
			i += 1
	else:
		if drink.lower() in drinks:
			price = prices[drinks.index(drink.lower())]
			update_success: bool = update_db(author.id, price, True)
			if update_success:
				await ctx.send("```You buy a glass of {} for ¤{}, and down it in a single gulp. You feel scammed.```".format(drink, price))
			else:
				await ctx.send("```You either cant afford that drink, or you dont even have an account```")
		else:
			await ctx.send("```I'm sorry, but I dont know how to make that drink```")


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
						"I sure hope there ain't a God, cause wow he hates us if he let you step foot on this earth, "
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
						", its like you rolled a nat 1 on life."
					]
	flen: int = len(finishers) - 1
	pidx: int = random.randint(0, plen)
	fidx: int = random.randint(0, flen)
	msg: str = (preambles[pidx] + name + finishers[fidx])
	await ctx.send("```{}```".format(msg))


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
						"You might be the closest we've ever come to irrefutable evidence that there is a benevolent God out there, "
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
						", I wish you the best!"
					]
	flen: int = len(finishers) - 1
	pidx: int = random.randint(0, plen)
	fidx: int = random.randint(0, flen)
	msg: str = (preambles[pidx] + name + finishers[fidx])
	await ctx.send("```{}```".format(msg))

bot.run(TOKEN)
