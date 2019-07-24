from cn_globals import *
import discord
from colorama import init

init()
from colorama import Fore as F
from colorama import Style as S
from colorama import Back as B


class CNDatabase:
    _db_separator: str = "/"
    _db_map_index: int = 0
    _db_map: list = [["", "", ""]]

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
                        self._db_map[self._db_map_index][0] = split[0]
                        self._db_map[self._db_map_index][1] = split[1]
                        self._db_map[self._db_map_index][2] = split[2]
                        print( B.BLUE + F.WHITE + 
                            "CNDB :: Pull -> Read user with ID: {} - ¤{} : {}xp".format(
                                self._db_map[self._db_map_index][0],
                                self._db_map[self._db_map_index][1],
                                self._db_map[self._db_map_index][2],
                            ) + S.RESET_ALL
                        )
                        self._db_map_index += 1
                except StopIteration:
                    print(
                        "CNDB :: Pull -> End of file encountered when reading through data stored on disk"
                    )

    def push(self) -> None:
        global DB

        with open(DB, "w") as clear:
            clear.write("")
        if self._db_map_index != 0:
            self._db_map_index = 0
            line: str = "0000000000000000"
            with open(DB, "a") as db:
                try:
                    line = "{}{}{}{}{}".format(
                        self._db_map[self._db_map_index][0],
                        self._db_separator,
                        self._db_map[self._db_map_index][1],
                        self._db_separator,
                        self._db_map[self._db_map_index][2]
                    )
                    db.write(line)
                    print( B.BLUE + F.WHITE + 
                        "CNDB :: Push -> Wrote user with ID: {} - ¤{} : {}xp".format(
                            self._db_map[self._db_map_index][0],
                            self._db_map[self._db_map_index][1],
                            self._db_map[self._db_map_index][2],
                        ) + S.RESET_ALL
                    )
                    self._db_map_index += 1
                except StopIteration:
                    print(
                        "CNDB :: Push -> End of file encountered when writing data to disk" 
                    )

    # Helper function. Registers a user to the bot DB
    def register(self, user: discord.User):
        userid: str = str(user.id)
        for user in self._db_map:
            if user[0] == userid:
                return None
        new_user: list = [userid, "1000", "0"]
        if self._db_map_index == 0:
            self._db_map[0] = new_user
        else:
            self._db_map.append(new_user)
        self._db_map_index += 1
        return -1

    # Helper function. Does all of the interfacing between the bot and the DB
    def update_db(self, userid, amount: int, sub: bool, isBet: bool = True, isXP: bool = False) -> int:
        for user in self._db_map:
            if user[0] == str(userid):
                if isXP:
                    user[2] = int(user[2]) + amount
                    return int(user[2])
                else:
                    if isBet:
                        if amount > int(user[1]):
                            return False
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
        self.register(user)
        return -1


    def print_internal_state(self) -> None:
        for user in self._db_map:
            print(user)
