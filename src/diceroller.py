import discord
import random
from discord.ext import commands

# Logging
import logging

info_logger = logging.getLogger('discord')
info_logger.setLevel(logging.INFO)
debug_logger = logging.getLogger('discord')
debug_logger.setLevel(logging.DEBUG)
info_handler = logging.FileHandler(filename='logs/info.cnlog', encoding='utf-8', mode='w')
debug_handler = logging.FileHandler(filename='logs/debug.cnlog', encoding='utf-8', mode='w')
info_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
info_logger.addHandler(info_handler)
debug_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
debug_logger.addHandler(debug_handler)

# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix='$')
client = discord.Client()
RIGGED = False
DB = "DB/database.cndb"
DBTMP = "DB/tmp.cncrypt"

# OC dont steal
TOKEN = ""
with open("enc/token.cncrypt", "r+") as tfile:
	TOKEN = tfile.readline()

# Roll a dice with a variable amount of sides
@bot.command()
async def roll(ctx, max: int):
	global RIGGED
	author = ctx.message.author
	print("({}) {} used $roll with {} sides".format(author.id, author.name, max))
	if max <= 1:
		# Someone will definitely attempt to roll a "0 sided die" and thats dumb
		await ctx.send("```Are you braindead? Do you not know how dice work?```")
		return
	roll = random.randint(1, max)
	if RIGGED:
		# If you wanna rigg a throw, make sure it always gets the max
		await ctx.send('```Rolled a {}```'.format(max))
		RIGGED = False
		print("Rig successfull, returning to standard, boring \"FAIR\" mode.")
	else:
		await ctx.send("```Rolled a {}```".format(roll))

# Rigg the next roll
@bot.command()
async def rigg(ctx):
	global RIGGED
	author = ctx.message.author
	print("({}) {} used $rigg | Is admin: {}".format(author.id, author.name, author.top_role.permissions.administrator))
	# Dont want the plebians to do this
	if author.top_role.permissions.administrator:
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
	author = ctx.message.author
	print("({}) {} used $rigged".format(author.id, author.name))
	await ctx.send("```How DARE you accuse me of rigging something as holy as a dice throw you degenerate manatee!```")

# Dice game, most of the code is DB stuff
@bot.command()
async def dg(ctx, bet):
	global RIGGED
	global DB
	global DBTMP
	author = ctx.message.author
	print("({}) {} used $dg for ¤{}".format(author.id, author.name, bet))
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
	line = "0000000000"
	# HERE WE GOOO
	with open(DB, "r+") as db:
		while line != "":
			try: # Use exceptions to find the EOF
				line = db.readline()
				if str(author.id) in line: # If we found the user
					split: list = line.split("/") # Get the balance and id seperately
					bal: str = split[1] 
					balint = int(bal)
					print("Old balance: {}".format(balint))
					if balint < int(bet): # cant bet more than you have
						await ctx.send("```Illegal bet -  You dont have that much!```")
						return
					if roll <= 55:
						balint -= int(bet) # lol loser
						await ctx.send("```I'm sorry {}, you lose with a roll of {}, losing ¤{}```".format(ctx.message.author.name, roll, bet))
					else:
						balint += int(bet) # gg no re
						await ctx.send("```Congrats {}, you win with a roll of {}, earning ¤{}```".format(ctx.message.author.name, roll, bet))
					print("New balance: {}".format(balint))
					bal = str(balint)
					split[1] = bal
					newline = split[0] + "/" + split[1] # make the new db entry
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
						print("Cleared TMP")
					return
			except StopIteration:
				print("End of file hit in DB search")	# EOF, tell them off for big dumbdumb
				await ctx.send("```Trying to gamble without money is kinda dumb```")
				return

# Register a user to the bot DB
@bot.command()
async def register(ctx):
	global DB
	author = ctx.message.author
	print("({}) {} used $register".format(author.id, author.name))
	line: str = "0000000000000"
	with open(DB, "r+") as db: # ah shit, here we go again
		while line != "":
			try:
				line = db.readline()		# check users
				if str(author.id) in line:
					split: list = line.split("/")
					print("({}) {} is already registered".format(author.id, author.name))
					bal: str = split[1]		# registering someone twice would be stupid
					await ctx.send("```You're already registered, {}! You have ¤{} currently```".format(author.name, bal))
					return
			except StopIteration:			# register them if they're not in the DB
				print("End of file hit in DB search")
		db.write(str(author.id) + "/1000\n")
	await ctx.send("**User {} has been registered!**".format(author.mention))

# Register another user to the bot DB
@bot.command()
async def register_other(ctx, user: discord.User):
	global DB
	author = ctx.message.author
	print("({}) {} used $register_other on ({}) {} | Is admin: {}".format(author.id, author.name, user.id, user.name, author.top_role.permissions.administrator))
	if author.top_role.permissions.administrator:
		line: str = "0000000000000"
		with open(DB, "r+") as db: # ah shit, here we go again
			while line != "":
				try:
					line = db.readline()		# check users
					if str(user.id) in line:
						split: list = line.split("/")
						print("({}) {} is already registered".format(user.id, user.name))
						bal: str = split[1]		# registering someone twice would be stupid
						await ctx.send("```{} is already registered! They have ¤{} currently```".format(user.name, bal))
						return
				except StopIteration:			# register them if they're not in the DB
					print("End of file hit in DB search")
			db.write(str(user.id) + "/1000\n")
		await ctx.send("**User {} has been registered!**".format(user.mention))

# Show a user their balance
@bot.command()
async def bal(ctx):
	global DB
	author = ctx.message.author
	print("({}) {} used $bal".format(author.id, author.name))
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
	global DB
	author = ctx.message.author
	print("({}) {} used $debug | Is admin: {}".format(author.id, author.name, author.top_role.permissions.administrator))
	# I really dont want people to spam debug info
	if author.top_role.permissions.administrator:
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
	global RIGGED
	global DB
	global DBTMP
	author = ctx.message.author
	print("({}) {} used $update on ({}) {} for ¤{} | Is admin: {}".format(author.id, author.name, user.id, user.name, amount, author.top_role.permissions.administrator))
	# I really dont want normal people to do this
	if author.top_role.permissions.administrator:
		line = "0000000000"
		# HERE WE GOOO
		with open(DB, "r+") as db:
			while line != "":
				try: # Use exceptions to find the EOF
					line = db.readline()
					if str(user.id) in line: # If we found the user
						print("User found for update ({})".format(user.id))
						split: list = line.split("/") # Get the balance and id seperately
						bal: str = split[1] 
						balint = int(bal)
						print("Old balance: {}".format(balint))
						balint += amount
						await ctx.send("```Balance of {} updated, You now have ¤{}```".format(user.name, balint))
						print("New balance: {}".format(balint))
						bal = str(balint)
						newline = str(user.id) + "/" + bal # make the new db entry
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
							print("Cleared TMP")
						return
				except StopIteration:
					print("End of file hit in DB search")	# EOF, tell them off for big dumbdumb
					await ctx.send("```They need an account to be eligible for a balance update```")
					return
	else:
		await ctx.send("```Thats a no from me dawg```")

bot.run(TOKEN)
