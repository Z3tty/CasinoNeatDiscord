import discord
import random
from discord.ext import commands

# Bot setup, and global variables that make things easier for me
bot = commands.Bot(command_prefix='$')
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
	# Dont want the plebians to do this
	if "satan" in [y.name.lower() for y in ctx.message.author.roles]:
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
	await ctx.send("```How DARE you accuse me of rigging something as holy as a dice throw you degenerate manatee!```")

# Dice game, most of the code is DB stuff
@bot.command()
async def dg(ctx, bet):
	global RIGGED
	global DB
	global DBTMP
	# get the current userid (db stuff)
	id = ctx.message.author.id
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
				if str(id) in line: # If we found the user
					split: list = line.split("/") # Get the balance and id seperately
					print("User found: ID -- {}, Splitlength -- {}, Listified -- {}".format(id, len(split), split))
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
					with open(DBTMP, "w") as clear: # clear the tmp file, just in case
						clear.write("")
					with open(DBTMP, "r+") as tmp:  # transfer all db info to temporary storage
						with open(DB, "r+") as db:
							dbline = db.readline()
							if dbline == line:			# write the new line instead of the old one
								tmp.write(newline+"\n")
							else:
								tmp.write(dbline+"\n")
					with open(DB, "w") as clear:		# clear the db
						clear.write("")
					with open(DB, "r+") as db:			# rewrite the db for future use
						with open(DBTMP, "r+") as tmp:
							db.write(tmp.readline())
					with open(DBTMP, "w") as clear:	# clear tmp to have it ready for the next pass
						clear.write("")
					return
			except StopIteration:
				print("End of file hit in DB search")	# EOF, tell them off for big dumbdumb
				await ctx.send("```Trying to gamble without money is kinda dumb```")
				return

# Register a user to the bot DB
@bot.command()
async def register(ctx):
	global DB
	id = ctx.message.author.id
	line: str = "0000000000000"
	with open(DB, "r+") as db: # ah shit, here we go again
		while line != "":
			try:
				line = db.readline()		# check users
				if str(id) in line:
					split: list = line.split("/")
					print("User found: ID -- {}, Splitlength -- {}, Listified -- {}".format(id, len(split), split))
					bal: str = split[1]		# registering someone twice would be stupid
					await ctx.send("```You're already registered, {}! You have ¤{} currently```".format(ctx.message.author.name, bal))
					return
			except StopIteration:			# register them if they're not in the DB
				print("End of file hit in DB search")
		db.write(str(id) + "/1000\n")
	await ctx.send("**User {} has been registered!**".format(ctx.message.author.mention))

# Show a user their balance
@bot.command()
async def bal(ctx):
	global DB
	id = ctx.message.author.id
	line: str = "0000000000000"
	with open(DB, "r+") as db: # getting really tired of file i/o
		while line != "":
			try:
				line = db.readline()
				if str(id) in line:
					split: list = line.split("/") # if we find them, respond with their balance and cease
					print("User found: ID -- {}, Splitlength -- {}, Listified -- {}".format(id, len(split), split))
					bal: str = split[1]
					await ctx.send("```{} has ¤{}```".format(ctx.message.author.name, bal))
					return
			except StopIteration:
				print("End of file hit in DB search") # let them know if they're stupid
				await ctx.send("```You have to be registered to have money, silly```")

# Get some debug info in the console
@bot.command()
async def debug(ctx):
	global DB
	# I really dont want people to spam debug info
	if "satan" in [y.name.lower() for y in ctx.message.author.roles]:
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
	# get the current userid (db stuff)
	id = user.id
	# I really dont want normal people to do this
	if "satan" in [y.name.lower() for y in ctx.message.author.roles]:
		line = "0000000000"
		# HERE WE GOOO
		with open(DB, "r+") as db:
			while line != "":
				try: # Use exceptions to find the EOF
					line = db.readline()
					if str(id) in line: # If we found the user
						split: list = line.split("/") # Get the balance and id seperately
						print("User found: ID -- {}, Splitlength -- {}, Listified -- {}".format(id, len(split), split))
						bal: str = split[1] 
						balint = int(bal)
						print("Old balance: {}".format(balint))
						balint += amount
						await ctx.send("```Balance of {} updated, You now have ¤{}```".format(user.name, balint))
						print("New balance: {}".format(balint))
						bal = str(balint)
						split[1] = bal
						newline = split[0] + "/" + split[1] # make the new db entry
						with open(DBTMP, "w") as clear: # clear the tmp file, just in case
							clear.write("")
						with open(DBTMP, "r+") as tmp:  # transfer all db info to temporary storage
							with open(DB, "r+") as db:
								dbline = db.readline()
								if dbline == line:			# write the new line instead of the old one
									tmp.write(newline+"\n")
								else:
									tmp.write(dbline+"\n")
						with open(DB, "w") as clear:		# clear the db
							clear.write("")
						with open(DB, "r+") as db:			# rewrite the db for future use
							with open(DBTMP, "r+") as tmp:
								db.write(tmp.readline())
						with open(DBTMP, "w") as clear:	# clear tmp to have it ready for the next pass
							clear.write("")
						return
				except StopIteration:
					print("End of file hit in DB search")	# EOF, tell them off for big dumbdumb
					await ctx.send("```They need an account to be eligible for a balance update```")
					return
	else:
		await ctx.send("```Thats a no from me dawg")

bot.run(TOKEN)
