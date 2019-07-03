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

from datetime import datetime
# Logging
import logging
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.CRITICAL)

# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix='?')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

RIGGED = False
DB = "DB/database.cndb"
DBTMP = "DB/tmp.cncrypt"
RANDOM_EVENT_CURRENTLY = False
RANDOM_EVENT_AMOUNT = 0

# OC dont steal
TOKEN = ""
with open("enc/token.cncrypt", "r+") as tfile:
	TOKEN = tfile.readline()

@bot.event
async def on_ready():
	now = datetime.now()
	game = discord.Game("with probabilities")
	await bot.change_presence(status=discord.Status.online, activity=game)
	date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
	print("Bot connected \t\t\t\t\t\t\t\t\t{} [V:ALPHA]".format(date_time))
	print("--------------------------------------------------------------------------------------------------------------")

@bot.event
async def on_message(message):
	global RANDOM_EVENT_CURRENTLY
	global RANDOM_EVENT_AMOUNT
	rnd = random.randint(0, 5000)
	if rnd < 100:
		RANDOM_EVENT_CURRENTLY = True
		RANDOM_EVENT_AMOUNT = random.randint(100, 10000)
		print("Random event for {} created".format(RANDOM_EVENT_AMOUNT))
		await message.channel.send("¤{} just materialized out of nothing, get it with `?grab`!".format(RANDOM_EVENT_AMOUNT))
	author = message.author
	if not author.bot:
		print("({}) {} > {}".format(author.id, author.name, message.content))
	else:
		print("[BOT] {}: {}".format(author.name, message.content))
	await bot.process_commands(message)


bot.remove_command('help')
# An help
@bot.command(aliases=['h', 'info', 'commands', 'c'])
async def help(ctx):
	"""
	help: 	
			displays a help message
	Requires:
			Nothing
	"""
	print("({}) {} used ?help".format(ctx.message.author.id, ctx.message.author.name))
	msg = discord.Embed(title="CN Diceroller", description="", color=0xff00ff)
	msg.add_field(name="?help", value="Displays this message. Alias=[h, info, commands, c]", inline=False)
	msg.add_field(name="?roll <dice> <sides>", value="Rolls some variable-sided dice and prints the result. Alias=[r]", inline=False)
	msg.add_field(name="?rigg", value="Nice try", inline=False)
	msg.add_field(name="?rigged", value="How dare you!", inline=False)
	msg.add_field(name="?gamble <bet>", value="Dicegame, betting ¤<bet> against a 100-sided roll, over 55 is a win. Alias=[55, 55x2, g, dg, bet]", inline=False)
	msg.add_field(name="?bal", value="Shows you how much money you have. Alias=[balance, eco, money]", inline=False)
	msg.add_field(name="?order <drink>", value="Buy a drink! userexperiencenotguaranteed", inline=False)
	msg.add_field(name="?pay <user> <amount>", value="Send someone your hard-earned money. Alias=[give]", inline=False)
	msg.add_field(name="?insult <name>", value="Generate an insult aimed at someone", inline=False)
	msg.add_field(name="?compliment <name>", value="Generate a compliment aimed at someone", inline=False)
	msg.add_field(name="?grab", value="Used to grab a randomly spawned event amount", inline=False)
	msg.add_field(name="?debug", value="(ADMIN) DB debug command", inline=False)
	msg.add_field(name="?update <@user> <amount>", value="(ADMIN) Give a user the provided amount", inline=False)
	msg.add_field(name="?raffle <prizeamount>", value="(ADMIN) Gives a random registered user a prize", inline=False)
	await ctx.send(embed=msg)

# Helper function. Registers a user to the bot DB
def register(user):
	global DB
	line: str = "0000000000000"
	with open(DB, "r+") as db: # ah shit, here we go again
		while line != "":
			try:
				line = db.readline()		# check users
				if str(user.id) in line:
					split: list = line.split("/")
					return None
			except StopIteration:			# register them if they're not in the DB
				print("End of file hit in DB search")
		db.write(str(user.id) + "/1000\n")
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
						bal = str(int(bal) - amount) # lol loser
					else:
						bal = str(int(bal) + amount) # gg no re
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

@bot.command()
async def grab(ctx):
	global RANDOM_EVENT_AMOUNT
	global RANDOM_EVENT_CURRENTLY
	author = ctx.author
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?roll for {} dice with {} sides | Rigged: {}".format(author.id, author.name, dice, sides, RIGGED))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	is_admin: bool = author.top_role.permissions.administrator
	print("({}) {} used ?rigg | Is admin: {}".format(author.id, author.name, is_admin))
	# Dont want the plebians to do this
	if is_admin:
		RIGGED = True
		print("It'll be our little secret ;)")
		# Hide the evidence
		await ctx.message.delete()
	else:
		# monkaS
		print("{} is onto us, keep an eye out :eyes:".format(ctx.message.author.name))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?rigged".format(author.id, author.name))
	await ctx.send("```How DARE you accuse me of rigging something as holy as a dice throw you degenerate manatee!```")

# Dice game, most of the code is DB stuff
@bot.command(aliases=['55', '55x2', 'g', 'dg', 'bet'])
async def gamble(ctx, bet: int = 0):
	"""
	dg: 	
			rolls a 100-sided die with a provided bet, and pays out double if above 55.
	Requires:
			User must be registered and have a sufficient balance to play the game
	"""
	global RIGGED
	author = ctx.message.author
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?dg for ¤{}".format(author.id, author.name, bet))
	if bet <= 0:
		await ctx.send("```You need to actually supply a bet, y'know```")
		return
	# get the current userid (db stuff)
	if RIGGED:
		# make sure we win if its rigged
		roll = random.randint(55, 100)
		# debug info
		print("{} rolled a {} in DG, Rigged: {}".format(ctx.message.author.name, roll, RIGGED))
		RIGGED = False
	else:
		# fair and boring roll
		roll = random.randint(1, 100)
		# debug info
		print("{} rolled a {} in DG, Rigged: {}".format(ctx.message.author.name, roll, RIGGED))
	update_success: bool = False
	if roll <= 55:
		update_success = update_db(author.id, int(bet), True)
		if update_success:
			await ctx.send("```I'm sorry, you just lost ¤{} with a roll of {}```".format(bet, roll))
			return
		else:
			await ctx.send("```You're either not registered(?register) or you do not have enough money to place that bet```")
			return
	else:
		update_success = update_db(author.id, int(bet), False)
		if update_success:
			await ctx.send("```Congrats, you just won ¤{} with a roll of {}```".format(bet, roll))
			return
		else:
			await ctx.send("```You're either not registered(?register) or you do not have enough money to place that bet```")
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?bal".format(author.id, author.name))
	line: str = "0000000000000"
	with open(DB, "r+") as db: # getting really tired of file i/o
		while line != "":
			try:
				line = db.readline()
				if str(author.id) in line:
					split: list = line.split("/") # if we find them, respond with their balance and cease
					bal: str = split[1]
					print("({}) {} has ¤{}".format(author.id, author.name, bal))
					await ctx.send("```{} has ¤{}```".format(author.name, bal))
					return
			except StopIteration:
				print("End of file hit in DB search") # let them know if they're stupid
				await ctx.send("```You have to be registered to have money, silly```")

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
	author = ctx.message.author
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	is_admin: bool = author.top_role.permissions.administrator
	print("({}) {} used ?debug | Is admin: {}".format(author.id, author.name, is_admin))
	# I really dont want people to spam debug info
	if is_admin:
		registered_users: int = 0
		total_balance: int = 0
		line: str = "0000000000000"
		with open(DB, "r+") as db: # getting really tired of file i/o
			while line != "":
				try:
					line = db.readline() # calculate totals and print individual info
					split: list = line.split("/")
					if len(split) >1:	 # ghost users are a thing
						bal: str = split[1]
						registered_users += 1
						total_balance += int(bal)
						print("User: {} - Balance: ¤{}".format(split[0], bal))
				except StopIteration:
					print("End of file hit in DB search") # in case the while fails
					break
		print("Total users: {}\t\tTotal balance: {}".format(registered_users, total_balance))
	else:
		await ctx.send("```Nice try, pleb```")

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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	is_admin: bool = author.top_role.permissions.administrator
	print("({}) {} used ?update on ({}) {} for ¤{} | Is admin: {}".format(author.id, author.name, user.id, user.name, amount, is_admin))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	is_admin: bool = author.top_role.permissions.administrator
	winner_id = ""
	print("({}) {} used ?raffle for ¤{} | Is admin: {}".format(author.id, author.name, prize, is_admin))
	if is_admin:
		user_ids: list = []
		line: str = "000000000"
		if RIGGED:
			winner_id = str(author.id)
			print("Rigged for : {}".format(winner_id))
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
						print("Hit end of db search")
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
	msg = register(user_from)
	if msg != None:
		await ctx.send(msg)
	msg = register(user_to)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?pay to transfer ¤{} to ({}) {}".format(user_from.id, user_from.name, amount, user_to.id, user_to.name))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?order for a glass of {}".format(author.id, author.name, drink))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	name: str = ""
	for arg in args:
		name += str(arg)
		name += " "
	name = name.rstrip()
	print("({}) {} used ?insult to insult {}".format(author.id, author.name, name))
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
	# Saving the indices for the console message later
	flen: int = len(finishers) - 1
	pidx: int = random.randint(0, plen)
	fidx: int = random.randint(0, flen)
	msg: str = (preambles[pidx] + name + finishers[fidx])
	print("Composed insult : {} \n//(Preamble[{}/{}], Finisher[{}/{}])//".format(msg, pidx, plen, fidx, flen))
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
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	name: str = ""
	for arg in args:
		name += str(arg)
		name += " "
	name = name.rstrip()
	print("({}) {} used ?compliment to compliment {}".format(author.id, author.name, name))
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
	# Saving the indices for the console message later
	flen: int = len(finishers) - 1
	pidx: int = random.randint(0, plen)
	fidx: int = random.randint(0, flen)
	msg: str = (preambles[pidx] + name + finishers[fidx])
	print("Composed compliment : {} \n//(Preamble[{}/{}], Finisher[{}/{}])//".format(msg, pidx, plen, fidx, flen))
	await ctx.send("```{}```".format(msg))


# Playing music - Requires PyNACL and Opus
""" To play youtube videos:
1) Verify the string
2) Download the video
3) Convert it to mp3
4) Play it locally
5) Verify that it has ended
6) Delete the downloaded video
@bot.command()
async def play(ctx, url: str):
	author = ctx.message.author
	msg = register(author)
	if msg != None:
		await ctx.send(msg)
	print("({}) {} used ?play with url: {}".format(author.id, author.name, url))
	if url.startswith("http:"):
		await ctx.send("```Excuse me, I'm not an idiot, use a secure protocol please (url starts with http:)```")
		return
	if url.startswith("https://you") or url.startswith("https://www.you"):
		if author.voice:
			channel = author.voice.channel
			vc = await channel.connect()
			vc.play(discord.FFmpegPCMAudio('testing.mp3'), after=lambda e: await disconnect(True))
		else:
			await ctx.send("```You must be in a VC to play music```")
	else:
		await ctx.send("```That doesnt look like youtube to me ...```")
		return
"""
bot.run(TOKEN)
