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
        new_user_weapon: dict = {
            "type": "WPN",
            "name": "Starter Sword",
            "rarity": "Common",
            "ATK": "10",
            "DEF": "2",
            "LUCK": "0",
        }
        new_user_armor: dict = {
            "type": "ARM",
            "name": "Starter Armor",
            "rarity": "Common",
            "ATK": "0",
            "DEF": "10",
            "LUCK": "0",
        }
        new_user_inv: list = []
        new_user_trades: list = []
        new_user.setprop("id", userid)
        new_user.setprop("balance", "1000")
        new_user.setprop("xp", "0")
        new_user.setprop("level", "1")
        new_user.setprop("last_daily", "0/0/0")
        new_user.setprop("daily_streak", "0")
        new_user.setprop("cookies_sent", "0")
        new_user.setprop("cookies_got", "0")
        new_user.setprop("thefts_failed", "0")
        new_user.setprop("rpg_attack", "10")
        new_user.setprop("rpg_defense", "10")
        new_user.setprop("rpg_luck", "1")
        new_user.setprop("weapon", json.dumps(new_user_weapon))
        new_user.setprop("armor", json.dumps(new_user_armor))
        new_user.setprop("inv", json.dumps(new_user_inv))
        new_user.setprop("trade_requests", json.dumps(new_user_trades))
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
                    level = 0
                    tmp = int(user.getprop("xp"))
                    old_level = int(user.getprop("level"))
                    while tmp > 0:
                        level += 1
                        if old_level < level:
                            atk = int(float(user.getprop("rpg_attack")))
                            defn = int(float(user.getprop("rpg_defense")))
                            luck = int(float(user.getprop("rpg_luck")))
                            user.setprop("rpg_attack", str(atk + random.randint(10, 100)))
                            user.setprop("rpg_defense", str(defn + random.randint(10, 100)))
                            user.setprop("rpg_luck", str(luck + random.randint(10, 100)))
                            old_level = level
                        tmp -= (1500 * level)
                    user.setprop("level", str(level))
                    
                    return int(user.getprop("xp"))
                else:
                    if isBet:
                        if amount > int(float(user.getprop("balance"))):
                            return -1
                        if sub:
                            user.setprop(
                                "balance", str(int(float(user.getprop("balance"))) - amount)
                            )
                        else:
                            user.setprop(
                                "balance", str(int(float(user.getprop("balance"))) + amount)
                            )
                    else:
                        if sub:
                            user.setprop(
                                "balance", str(int(float(user.getprop("balance"))) - amount)
                            )
                        else:
                            user.setprop(
                                "balance", str(int(float(user.getprop("balance"))) + amount)
                            )
                    return int(float(user.getprop("balance")))
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
            user.setprop(
                "balance",
                str(
                    int(float(user.getprop("balance")))
                    + DAILY_BONUS
                    + (DAILY_BONUS * current_streak * DAILY_STREAK_SCALAR)
                ),
            )
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


    def get_character(self, uid) -> dict:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return {None:None}
        weapon_data: dict = json.loads(user.getprop("weapon"))
        armor_data: dict = json.loads(user.getprop("armor"))
        character_data : dict = {
            "LV": user.getprop("level"),
            "ATK": str(int(float(user.getprop("rpg_attack"))) + int(float(weapon_data["ATK"])) + int(float(armor_data["ATK"]))),
            "DEF": str(int(float(user.getprop("rpg_defense"))) + int(float(weapon_data["DEF"])) + int(float(armor_data["DEF"]))),
            "LUCK": str(int(float(user.getprop("rpg_luck"))) + int(float(weapon_data["LUCK"])) + int(float(armor_data["LUCK"]))),
        } 
        return character_data
    
    def add_item(self, uid, item: dict) -> None:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty(): return
        tmp: list = json.loads(user.getprop("inv"))
        if len(tmp) >= 16:
            return
        tmp.append(json.dumps(item))
        user.setprop("inv", json.dumps(tmp))
    
    def get_player_data(self, uid) -> dict:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return {None:None}
        return user.getall()
    
    def get_inventory(self, uid) -> list:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return [None]
        return json.loads(user.getprop("inv"))

    def update_inventory(self, uid, equipid: int) -> bool:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return [None]
        istring = ""
        inv = json.loads(user.getprop("inv"))
        item = json.loads(inv[equipid])
        if item["type"] == "WPN":
            istring = user.getprop("weapon")
            user.setprop("weapon", json.dumps(item))
        else:
            istring = user.getprop("armor")
            user.setprop("armor", json.dumps(item))
        inv[equipid] = istring
        user.setprop("inv", json.dumps(inv))
        return item["type"] == "WPN"
    
    def sell_item(self, uid, equipid: int) -> (int, dict):
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return {None:None}
        inv = json.loads(user.getprop("inv"))
        item = json.loads(inv[equipid])
        del inv[equipid]
        user.setprop("inv", json.dumps(inv))
        value: int = int(float(item["ATK"])) + int(float(item["DEF"])) + int(float(item["LUCK"]))
        if item["rarity"] == "Artifact":
            value *= 5
        if item["rarity"] == "Legendary":
            value *= 4
        if item["rarity"] == "Epic":
            value *= 3
        if item["rarity"] == "Rare":
            value *= 2
        if item["rarity"] == "Uncommon":
            value *= 1.5
        self.update_db(uid, value, False, False)
        print(value)
        print(item)
        return (value, item)

    def get_trades(self, uid) -> list:
        user: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
        if user.empty():
            return [None]
        return json.loads(user.getprop("trade_requests"))
    
    def resolve_trade(self, uid, tid: int, accept: bool) -> bool:
        user: CNDBUser = CNDBUser()
        recp: CNDBUser = CNDBUser()
        trades: list = self.get_trades(uid)
        trade: dict = trades[tid]
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
            if u.getprop("id") == trade["player_id"]:
                recp = u
        if user.empty() or recp.empty() or user.getprop("id") == recp.getprop("id"):
            return False
        u0_item = trade["item0"]
        u1_item = trade["item1"]
        u0_inv = self.get_inventory(uid)
        u1_inv = self.get_inventory(recp.getprop("id"))
        if accept:
            u0_inv.append(json.dumps(u0_item))
            u1_inv.append(json.dumps(u1_item))
            user.setprop("inv", json.dumps(u0_inv))
            recp.setprop("inv", json.dumps(u1_inv))
        else:
            u0_inv.append(json.dumps(u1_item))
            u1_inv.append(json.dumps(u0_item))
            user.setprop("inv", json.dumps(u0_inv))
            recp.setprop("inv", json.dumps(u1_inv))
        del trades[tid]
        user.setprop("trade_requests", json.dumps(trades))
        return True
    
    def add_trade(self, uid, recipient, eid, reid) -> bool:
        user: CNDBUser = CNDBUser()
        recp: CNDBUser = CNDBUser()
        for u in self._db_map:
            if u.getprop("id") == str(uid):
                user = u
            if u.getprop("id") == str(recipient):
                recp = u
        if user.empty() or recp.empty() or user.getprop("id") == recp.getprop("id"):
            return False
        uinv = self.get_inventory(uid)
        rinv = self.get_inventory(recipient)
        item_0 = json.loads(uinv[eid])
        item_1 = json.loads(rinv[reid])
        del uinv[eid]
        del rinv[reid]
        user.setprop("inv", json.dumps(uinv))
        recp.setprop("inv", json.dumps(rinv))
        trade: dict = {"player_id": user.getprop("id"), "item0": item_0, "item1": item_1}
        trades: list = self.get_trades(recp.getprop("id"))
        trades.append(trade)
        recp.setprop("trade_requests", json.dumps(trades))
        return True
