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
# I'm really sorry but globals are really the easiest way of handling this
RIGGED = False
DB = "DB/database.cndb"
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
DAILY_BONUS = 500
DAILY_STREAK_SCALAR = 2
FINE_AMOUNT = 500
BRIBE_PRICE = 10000
LOTTO_REWARD = 10000000
VERSION = "1.5"

# OC dont steal
TOKEN = ""
with open("enc/token.cncrypt", "r+") as tfile:
    TOKEN = tfile.readline()
TOKEN = TOKEN.rstrip().lstrip()
