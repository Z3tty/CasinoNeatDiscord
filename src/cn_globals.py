# I'm really sorry but globals are really the easiest way of handling this
RIGGED = False
DB = "DB/database.cndb"
DBTMP = "DB/tmp.cncrypt"
AUTHOR = "Zet#1024 (github.com/ZexZee)"
RANDOM_EVENT_CURRENTLY = False
RANDOM_EVENT_AMOUNT = 0
CRATE_SPAWNED = False
CRATE_GIVES_XP = False
CRATE_REWARD_AMOUNT = 0
FILTER_USERS = False
FILTER_BOTS = False
FILTER_LOGS = False
DB_PUSH_TIMEOUT = 60.0
HAS_CHANGED = False

# OC dont steal
TOKEN = ""
with open("enc/token.cncrypt", "r+") as tfile:
    TOKEN = tfile.readline()
TOKEN = TOKEN.rstrip().lstrip()
