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


class CNDatabase:
    _db_separator: str = "/"
    _db_map_index: int = 0
    _db_map: list = []

    def __init__(self):
        pass

    def pull(self) -> None:
        global DB

        line: str = "0000000000000000"
        with open(DB, "r") as db:
            while line != "":
                try:
                    line = db.readline().rstrip().lstrip()  # check users
                    split: list = line.split(self._db_separator)
                    if len(split) > 2:
                        usr: list = split
                        self._db_map.append(usr)
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Pull->Read user with ID:{} - ¤{} : {}xp : Last Daily:{}, Daily Streak:{}, Sent cookies:{}, Recieved cookies:{}, Failed thefts: {}".format(
                                self._db_map[self._db_map_index][0],
                                self._db_map[self._db_map_index][1],
                                self._db_map[self._db_map_index][2],
                                self._db_map[self._db_map_index][3],
                                self._db_map[self._db_map_index][4],
                                self._db_map[self._db_map_index][5],
                                self._db_map[self._db_map_index][6],
                                self._db_map[self._db_map_index][7],
                            )
                            + S.RESET_ALL
                        )
                        self._db_map_index += 1
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
            line: str = "0000000000000000"
            with open(DB, "a") as db:
                while line != "" and self._db_map_index < len(self._db_map):
                    try:
                        line = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(
                            self._db_map[self._db_map_index][0],
                            self._db_separator,
                            self._db_map[self._db_map_index][1],
                            self._db_separator,
                            self._db_map[self._db_map_index][2],
                            self._db_separator,
                            self._db_map[self._db_map_index][3],
                            self._db_separator,
                            self._db_map[self._db_map_index][4],
                            self._db_separator,
                            self._db_map[self._db_map_index][5],
                            self._db_separator,
                            self._db_map[self._db_map_index][6],
                            self._db_separator,
                            self._db_map[self._db_map_index][7],
                        )
                        db.write(line)
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Push->Wrote user with ID:{} - ¤{} : {}xp : Last Daily:{}, Daily Streak:{}, Sent cookies:{}, Recieved cookies:{}, Failed thefts: {}".format(
                                self._db_map[self._db_map_index][0],
                                self._db_map[self._db_map_index][1],
                                self._db_map[self._db_map_index][2],
                                self._db_map[self._db_map_index][3],
                                self._db_map[self._db_map_index][4],
                                self._db_map[self._db_map_index][5],
                                self._db_map[self._db_map_index][6],
                                self._db_map[self._db_map_index][7],
                            )
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
            if user[0] == userid:
                return None
        new_user: list = [userid, "1000", "0", "-1", "0", "0", "0", "0"]
        self._db_map.append(new_user)
        line = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(
                            self._db_map[self._db_map_index][0],
                            self._db_separator,
                            self._db_map[self._db_map_index][1],
                            self._db_separator,
                            self._db_map[self._db_map_index][2],
                            self._db_separator,
                            self._db_map[self._db_map_index][3],
                            self._db_separator,
                            self._db_map[self._db_map_index][4],
                            self._db_separator,
                            self._db_map[self._db_map_index][5],
                            self._db_separator,
                            self._db_map[self._db_map_index][6],
                            self._db_separator,
                            self._db_map[self._db_map_index][7],
        )
        with open(DB, "a") as db:
            db.write(line)
        self._db_map_index += 1
        return -1

    # Does all of the interfacing between the bot and the DB
    def update_db(
        self, userid, amount: int, sub: bool, isBet: bool = True, isXP: bool = False
    ) -> int:
        global HAS_CHANGED_DB
        global HAS_CHANGED_RPG

        for user in self._db_map:
            if user[0] == str(userid):
                HAS_CHANGED_DB = True
                HAS_CHANGED_RPG = True
                if isXP:
                    if sub:
                        user[2] = int(user[2]) - amount
                    else:
                        user[2] = int(user[2]) + amount
                    return int(user[2])
                else:
                    if isBet:
                        if amount > int(user[1]):
                            return -1
                        if sub:
                            user[1] = str(int(user[1]) - amount)
                        else:
                            user[1] = str(int(user[1]) + amount)
                    else:
                        if sub:
                            user[1] = str(int(user[1]) - amount)
                        else:
                            user[1] = str(int(user[1]) + amount)
                    return int(user[1])
        return -1

    def print_internal_state(self) -> None:
        for user in self._db_map:
            print(user)

    def update_daily(self, userid) -> (int, int):
        global DAILY_BONUS
        global DAILY_STREAK_SCALAR

        allowed = False
        user = []
        index = 0
        for u in self._db_map:
            if u[0] == str(userid):
                user = u
                break
            else:
                index += 1
        if user == []:
            print("Error: No user found")
            print("Got: {}".format(user))
            return (-1, -1)
        last = user[3]
        now = dt.today()
        day: str = str(now.day)
        month: str = str(now.month)
        if int(day) < 10:
            day = "0{}".format(day)
        if int(month) < 10:
            month = "0{}".format(month)
        daily_str = str(str(now.year) + month + day)
        last_month: str = str(last[len(last) - 4]) + str(last[len(last) - 3])
        last_day: str = str(last[len(last) - 2]) + str(last[len(last) - 1])
        if last_month in ["01", "03", "05", "07", "08", "10", "12"]:
            if day == "01" and last_day == "31":
                last = str(int(daily_str) - 1)
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
            user[3] = daily_str
            current_streak = int(user[4])
            if int(last) == int(daily_str) - 1:
                current_streak += 1
            else:
                current_streak = 0
            user[1] = str(
                int(user[1])
                + DAILY_BONUS
                + (DAILY_BONUS * current_streak * DAILY_STREAK_SCALAR)
            )
            user[4] = str(current_streak)
            self._db_map[index] = user
            return (
                DAILY_BONUS + (DAILY_BONUS * current_streak * DAILY_STREAK_SCALAR),
                current_streak,
            )
        else:
            return (-1, -1)

    def send_cookie(self, userid_sender, userid_reciever) -> (int, int):
        sender = []
        reciever = []
        sender_idx = 0
        reciever_idx = 0
        index = 0
        for u in self._db_map:
            if u[0] == str(userid_sender):
                sender = u
                sender_idx = index
            if u[0] == str(userid_reciever):
                reciever = u
                reciever_idx = index
            index += 1
        if sender == [] or reciever == []:
            return (-1, -1)
        sender_sent = int(sender[5]) + 1
        sender_recv = int(sender[6])
        reciever_recv = int(reciever[6]) + 1
        self._db_map[sender_idx][5] = str(sender_sent)
        self._db_map[reciever_idx][6] = str(reciever_recv)
        return (sender_sent, sender_recv)

    def get_user_list(self):
        ids = []
        for user in self._db_map:
            ids.append(user[0])
        return ids

    def update_user_thefts(
        self, userid, reset: bool = False, fetch: bool = False
    ) -> int:
        user = []
        index = 0
        for u in self._db_map:
            if u[0] == str(userid):
                user = u
                break
            index += 1
        if fetch:
            return int(user[7])
        if reset:
            user[7] = "0"
            self._db_map[index] = user
            return 0
        else:
            tmp = int(user[7])
            user[7] = str(tmp + 1)
            self._db_map[index] = user
            return tmp + 1
