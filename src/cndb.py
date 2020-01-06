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
from cn_globals import *
import discord
import random
from colorama import init

init()
from colorama import Fore as F
from colorama import Style as S
from colorama import Back as B
from datetime import datetime as dt
import json
from user import CNDBUser


class CNDatabase:
    _db_map_index: int = 0
    _db_map: list = []

    def __init__(self):
        pass

    def pull(self) -> None:
        global DB

        line: str = "0000000000000000"
        with open(DB, "r") as db:
            line = db.readline()
            while line != "":      
                try:
                    u: CNDBUser = CNDBUser()
                    u.setall(json.loads(line))
                    if not u.empty():
                        self._db_map.append(u)
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Pull->Read user {}".format(u.getall())
                            + S.RESET_ALL
                        )
                        self._db_map_index += 1
                    line = db.readline()
                except StopIteration:
                    print(
                        "CNDB::Pull->End of file encountered when reading through data stored on disk"
                    )

    def push(self) -> None:
        global DB
        global HAS_CHANGED_DB

        if self._db_map_index != 0 and HAS_CHANGED_DB:
            with open(DB, "w") as clear:
                clear.write("")
            self._db_map_index = 0
            with open(DB, "a") as db:
                while self._db_map_index < len(self._db_map):
                    try:
                        u: CNDBUser = self._db_map[self._db_map_index]
                        db.write(json.dumps(u.getall()) + "\n")
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Push->Wrote user {}".format(u.getall())
                            + S.RESET_ALL
                        )
                        self._db_map_index += 1
                    except StopIteration:
                        print(
                            "CNDB::Push->End of file encountered when writing data to disk"
                        )
                HAS_CHANGED_DB = False

    # Registers a user to the bot DB
    def register(self, user: discord.User):
        global DB

        userid: str = str(user.id)
        for user in self._db_map:
            if user.getprop("id") == userid:
                return None
        new_user: CNDBUser = CNDBUser()
        new_user.setprop("id", userid)
        new_user.setprop("balance", "1000")
        new_user.setprop("xp", "0")
        new_user.setprop("last_daily", "0/0/0")
        new_user.setprop("daily_streak", "0")
        new_user.setprop("cookies_sent", "0")
        new_user.setprop("cookies_got", "0")
        new_user.setprop("thefts_failed", "0")
        self._db_map.append(new_user)
        with open(DB, "a") as db:
            db.write(json.dumps(new_user.getall()) + "\n")
        self._db_map_index += 1
        return -1

    # Does all of the interfacing between the bot and the DB
    def update_db(
        self, userid, amount: int, sub: bool, isBet: bool = True, isXP: bool = False
    ) -> int:
        global HAS_CHANGED_DB

        for user in self._db_map:
            if user.getprop("id") == str(userid):
                HAS_CHANGED_DB = True
                if isXP:
                    if sub:
                        user.setprop("xp", str(int(user.getprop("xp")) - amount))
                    else:
                        user.setprop("xp", str(int(user.getprop("xp")) + amount))
                    return int(user.getprop("xp"))
                else:
                    if isBet:
                        if amount > int(user.getprop("balance")):
                            return -1
                        if sub:
                            user.setprop("balance", str(int(user.getprop("balance")) - amount))
                        else:
                            user.setprop("balance", str(int(user.getprop("balance")) + amount))
                    else:
                        if sub:
                            user.setprop("balance", str(int(user.getprop("balance")) - amount))
                        else:
                            user.setprop("balance", str(int(user.getprop("balance")) + amount))
                    return int(user.getprop("balance"))
        return -1

    def print_internal_state(self) -> None:
        for user in self._db_map:
            print(user.getall())

    def update_daily(self, userid) -> (int, int):
        global DAILY_BONUS
        global DAILY_STREAK_SCALAR

        allowed = False
        user: CNDBUser = CNDBUser()
        index = 0
        for u in self._db_map:
            if u.getprop("id") == str(userid):
                user = u
                break
            else:
                index += 1
        if user.empty():
            print("Error: No user found")
            print("Got: {}".format(user.getall()))
            return (-1, -1)
        last: str = user.getprop("last_daily")
        llist: list = last.split("/")
        now = dt.today()
        day: str = str(now.day)
        month: str = str(now.month)
        if int(day) < 10:
            day = "0{}".format(day)
        if int(month) < 10:
            month = "0{}".format(month)
        daily_str = "{}/{}/{}".format(now.year, month, day)
        last_month: str = llist[1]
        last_day: str = llist[2]
        if last_month in ["01", "03", "05", "07", "08", "10", "12"]:
            if day == "01" and last_day == "31":
                last = str(int(daily_str.replace("/", "")) - 1)
        if last_month == "02":
            if day == "01" and last_day == "28":
                last = str(int(daily_str) - 1)
        else:
            if day == "01" and last_day == "30":
                last = str(int(daily_str) - 1)
        print("Last daily: {}, todays daily: {}".format(last, daily_str))
        if last != daily_str:
            allowed = True
        if allowed:
            user.setprop("last_daily", daily_str)
            current_streak = int(user.getprop("daily_streak"))
            if int(last.replace("/", "")) == int(daily_str.replace("/", "")) - 1:
                current_streak += 1
            else:
                current_streak = 0
            user.setprop("balance", str(
                int(user.getprop("balance"))
                + DAILY_BONUS
                + (DAILY_BONUS * current_streak * DAILY_STREAK_SCALAR)
            ))
            user.setprop("daily_streak", str(current_streak))
            self._db_map[index] = user
            return (
                DAILY_BONUS + (DAILY_BONUS * current_streak * DAILY_STREAK_SCALAR),
                current_streak,
            )
        else:
            return (-1, -1)

    def send_cookie(self, userid_sender, userid_reciever) -> (int, int):
        sender: CNDBUser = CNDBUser()
        reciever: CNDBUser = CNDBUser()
        sender_idx = 0
        reciever_idx = 0
        index = 0
        for u in self._db_map:
            if u.getprop("id") == str(userid_sender):
                sender = u
                sender_idx = index
            if u.getprop("id") == str(userid_reciever):
                reciever = u
                reciever_idx = index
            index += 1
        if sender.empty() or reciever.empty():
            return (-1, -1)
        sender_sent = int(sender.getprop("cookies_sent")) + 1
        sender_recv = int(sender.getprop("cookies_got"))
        reciever_recv = int(reciever.getprop("cookies_got")) + 1
        self._db_map[sender_idx].setprop("cookies_sent", str(sender_sent))
        self._db_map[reciever_idx].setprop("cookies_got", str(reciever_recv))
        return (sender_sent, sender_recv)

    def get_user_list(self):
        ids = []
        for user in self._db_map:
            ids.append(user.getprop("id"))
        return ids
    
    def get_users(self):
        return self._db_map

    def update_user_thefts(
        self, userid, reset: bool = False, fetch: bool = False
    ) -> int:
        user: CNDBUser = CNDBUser()
        index = 0
        for u in self._db_map:
            if u.getprop("id") == str(userid):
                user = u
                break
            index += 1
        if fetch:
            return int(user.getprop("thefts_failed"))
        if reset:
            user.setprop("thefts_failed", "0")
            self._db_map[index] = user
            return 0
        else:
            tmp = int(user.getprop("thefts_failed"))
            user.setprop("thefts_failed", str(tmp + 1))
            self._db_map[index] = user
            return tmp + 1
