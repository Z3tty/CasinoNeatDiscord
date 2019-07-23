from cn_globals import *
import discord

class CNDatabase:
	def __init__(self):
		pass
	# Helper function. Registers a user to the bot DB
	def register(self, user: discord.User):
	    global DB
	    global DB_LEVEL

	    line: str = "0000000000000"
	    with open(DB, "r+") as db:  # ah shit, here we go again
	        while line != "":
	            try:
	                line = db.readline()  # check users
	                if str(user.id) in line:
	                    split: list = line.split("/")
	                    return None
	            except StopIteration:  # register them if they're not in the DB
	                debug_console_log("register", user, "Error: Hit EOF before end of loop")
	        db.write(str(user.id) + "/1000\n")
	    line = "0000000000000"
	    with open(DB_LEVEL, "r+") as ldb:  # ah shit, here we go again
	        while line != "":
	            try:
	                line = ldb.readline()  # check users
	                if str(user.id) in line:
	                    split: list = line.split("/")
	                    return None
	            except StopIteration:  # register them if they're not in the DB
	                debug_console_log("register", user, "Error: Hit EOF before end of loop")
	        ldb.write(str(user.id) + "/0\n")
	    return "```User {} has been registered!```".format(user.name)

	# Helper function. Does all of the interfacing between the bot and the DB
	def update_db(self, userid, amount: int, sub: bool, isBet: bool = True) -> bool:
	    global DB
	    global DBTMP

	    line = "0000000000"
	    # HERE WE GOOO
	    with open(DB, "r+") as db:
	        while line != "":
	            try:  # Use exceptions to find the EOF
	                line = db.readline()
	                if str(userid) in line:  # If we found the user
	                    split: list = line.split("/")  # Get the balance and id seperately
	                    bal: str = split[1]
	                    if int(bal) < amount and isBet:  # cant bet more than you have
	                        return False
	                    if sub:
	                        bal = str(int(bal) - amount)
	                    else:
	                        bal = str(int(bal) + amount)
	                    newline = str(userid) + "/" + str(bal)  # make the new db entry
	                    tmpdata = "0000000"
	                    with open(DBTMP, "w") as clear:  # clear the tmp file, just in case
	                        clear.write("")
	                    with open(
	                        DBTMP, "r+"
	                    ) as tmp:  # transfer all db info to temporary storage
	                        with open(DB, "r+") as db:
	                            while tmpdata != "":
	                                dbline = db.readline()
	                                tmpdata = dbline
	                                if (
	                                    dbline == line
	                                ):  # write the new line instead of the old one
	                                    tmp.write(newline + "\n")
	                                else:
	                                    tmp.write(dbline + "\n")
	                    tmpdata = "0000000"
	                    with open(DB, "w") as clear:  # clear the db
	                        clear.write("")
	                    with open(DB, "r+") as db:  # rewrite the db for future use
	                        with open(DBTMP, "r+") as tmp:
	                            while tmpdata != "":
	                                tmpdata = tmp.readline()
	                                if tmpdata != "\n":
	                                    db.write(tmpdata)
	                    with open(
	                        DBTMP, "w"
	                    ) as clear:  # clear tmp to have it ready for the next pass
	                        clear.write("")
	                    return True
	            except StopIteration:
	                return False
	# Helper function. Does all of the interfacing between the bot and the DB
	# Returns -1 if not registered, then registers.
	def update_level_db(self, user, amount: int) -> int:
	    global DB_LEVEL
	    global DBTMP

	    xp_after_update: int = 0
	    userid = user.id
	    line = "0000000000"
	    # HERE WE GOOO
	    with open(DB_LEVEL, "r+") as db:
	        while line != "":
	            try:  # Use exceptions to find the EOF
	                line = db.readline()
	                if str(userid) in line:  # If we found the user
	                    split: list = line.split("/")  # Get the balance and id seperately
	                    xp: str = split[1]
	                    xp_after_update = int(xp) + amount
	                    newline = (
	                        str(userid) + "/" + str(xp_after_update)
	                    )  # make the new db entry
	                    tmpdata = "0000000"
	                    with open(DBTMP, "w") as clear:  # clear the tmp file, just in case
	                        clear.write("")
	                    with open(
	                        DBTMP, "r+"
	                    ) as tmp:  # transfer all db info to temporary storage
	                        with open(DB_LEVEL, "r+") as db:
	                            while tmpdata != "":
	                                dbline = db.readline()
	                                tmpdata = dbline
	                                if (
	                                    dbline == line
	                                ):  # write the new line instead of the old one
	                                    tmp.write(newline + "\n")
	                                else:
	                                    tmp.write(dbline + "\n")
	                    tmpdata = "0000000"
	                    with open(DB_LEVEL, "w") as clear:  # clear the db
	                        clear.write("")
	                    with open(DB_LEVEL, "r+") as db:  # rewrite the db for future use
	                        with open(DBTMP, "r+") as tmp:
	                            while tmpdata != "":
	                                tmpdata = tmp.readline()
	                                if tmpdata != "\n":
	                                    db.write(tmpdata)
	                    with open(
	                        DBTMP, "w"
	                    ) as clear:  # clear tmp to have it ready for the next pass
	                        clear.write("")
	                    return xp_after_update
	            except StopIteration:
	                register(user)
	                return -1
