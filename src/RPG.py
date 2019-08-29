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
from enum import Enum

RPG_Item_WeaponTypes: list = ["Sword", "Spear", "Staff", "Wand", "Axe", "Hammer", "Bow"]
RPG_Item_ArmorTypes: list = ["Robe", "Leather Armor", "Plate Armor"]
RPG_Item_OffTypes: list = ["Orb", "Book", "Shield"]
RPG_Item_NegativePrefixes: list = ["Battered", "Rusty", "Cracked", "Broken"]
RPG_Item_PositivePrefixes: list = [
    "Honed",
    "Fine",
    "Tempered",
    "Legendary",
    "Exalted",
    "Smoldering",
    "Powerful",
    "Magical",
]
RPG_Item_Rare_Suffixes: list = [
    "of the Void",
    "of the Skies",
    "of Thundering Might",
    "of Darkness",
    "of the Sun",
    "of Luck",
]


class RPGItem:
    item_name = ""
    item_stats: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
    prefix_stat_boosts: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
    suffix_stat_boosts: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
    item_slot = -1
    prefix = ""
    suffix = ""
    item_description = ""

    def __init__(self):
        self.item_name = ""
        self.item_stats: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
        self.prefix_stat_boosts: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
        self.suffix_stat_boosts: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
        self.item_slot = -1
        self.prefix = ""
        self.suffix = ""
        self.item_description = ""

    def stringify(self) -> str:
        istr: str = str(self.item_name) + "|" + str(self.item_stats["ATK"]) + "|" + str(
            self.item_stats["DEF"]
        ) + "|" + str(self.item_stats["HP"]) + "|" + str(
            self.item_stats["CRIT"]
        ) + "|" + str(
            self.item_slot
        ) + "|" + self.prefix + "|" + str(
            self.prefix_stat_boosts["ATK"]
        ) + "|" + str(
            self.prefix_stat_boosts["DEF"]
        ) + "|" + str(
            self.prefix_stat_boosts["HP"]
        ) + "|" + str(
            self.prefix_stat_boosts["CRIT"]
        ) + "|" + self.suffix + "|" + str(
            self.suffix_stat_boosts["ATK"]
        ) + "|" + str(
            self.suffix_stat_boosts["DEF"]
        ) + "|" + str(
            self.suffix_stat_boosts["HP"]
        ) + "|" + str(
            self.suffix_stat_boosts["CRIT"]
        )
        return istr


class RPGItemCreator:
    def __init__(self):
        pass

    def create_random(self, difficulty: int = 1, isRaidDrop: bool = False) -> RPGItem:
        item = RPGItem()
        item_type = ""
        item.item_slot = random.randint(0, 2)
        print(item.item_slot)
        if item.item_slot == 0:
            item.item_stats["ATK"] = random.randint(2, 15 * difficulty)
            item.item_stats["CRIT"] = random.randint(2, 15 * difficulty)
            item_type = RPG_Item_WeaponTypes[
                random.randint(0, len(RPG_Item_WeaponTypes) - 1)
            ]
            print(item_type)
            has_prefix = random.randint(0, 10) > 5
            if has_prefix:
                has_beneficial_prefix = random.randint(0, 10) > 3
                if has_beneficial_prefix:
                    item.prefix = RPG_Item_PositivePrefixes[
                        random.randint(0, len(RPG_Item_PositivePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = random.randint(0, 10 * difficulty)
                    item.prefix_stat_boosts["DEF"] = random.randint(0, 10 * difficulty)
                    item.prefix_stat_boosts["HP"] = random.randint(0, 10 * difficulty)
                    item.prefix_stat_boosts["CRIT"] = random.randint(0, 10 * difficulty)
                else:
                    item.prefix = RPG_Item_NegativePrefixes[
                        random.randint(0, len(RPG_Item_NegativePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["DEF"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["HP"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["CRIT"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
        elif item.item_slot == 1:
            item.item_stats["ATK"] = random.randint(0 + difficulty, 15 * difficulty)
            item.item_stats["CRIT"] = random.randint(0 + difficulty, 15 * difficulty)
            item.item_stats["DEF"] = random.randint(0 + difficulty, 15 * difficulty)
            item.item_stats["HP"] = random.randint(0 + difficulty, 15 * difficulty)
            item_type = RPG_Item_OffTypes[random.randint(0, len(RPG_Item_OffTypes) - 1)]
            print(item_type)
            has_prefix = random.randint(0, 10) > 5
            if has_prefix:
                has_beneficial_prefix = random.randint(0, 10) > 3
                if has_beneficial_prefix:
                    item.prefix = RPG_Item_PositivePrefixes[
                        random.randint(0, len(RPG_Item_PositivePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["DEF"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["HP"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["CRIT"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                else:
                    item.prefix = RPG_Item_NegativePrefixes[
                        random.randint(0, len(RPG_Item_NegativePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["DEF"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["HP"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["CRIT"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )

        elif item.item_slot == 2:
            item.item_stats["DEF"] = random.randint(2, 15 * difficulty)
            item.item_stats["HP"] = random.randint(2, 15 * difficulty)
            item_type = RPG_Item_ArmorTypes[
                random.randint(0, len(RPG_Item_ArmorTypes) - 1)
            ]
            print(item_type)
            has_prefix = random.randint(0, 10) > 5
            if has_prefix:
                has_beneficial_prefix = random.randint(0, 10) > 3
                if has_beneficial_prefix:
                    item.prefix = RPG_Item_PositivePrefixes[
                        random.randint(0, len(RPG_Item_PositivePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["DEF"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["HP"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                    item.prefix_stat_boosts["CRIT"] = random.randint(
                        0 + difficulty, 10 * difficulty
                    )
                else:
                    item.prefix = RPG_Item_NegativePrefixes[
                        random.randint(0, len(RPG_Item_NegativePrefixes) - 1)
                    ]
                    item.prefix_stat_boosts["ATK"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["DEF"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["HP"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
                    item.prefix_stat_boosts["CRIT"] = -random.randint(
                        0 - difficulty, 10 - difficulty
                    )
        else:
            print("ERROR")
            return
        if isRaidDrop:
            item.suffix = RPG_Item_Rare_Suffixes[
                random.randint(0, len(RPG_Item_Rare_Suffixes) - 1)
            ]
            item.suffix_stat_boosts["ATK"] = random.randint(
                0 + difficulty, 50 * difficulty
            )
            item.suffix_stat_boosts["DEF"] = random.randint(
                0 + difficulty, 50 * difficulty
            )
            item.suffix_stat_boosts["HP"] = random.randint(
                0 + difficulty, 50 * difficulty
            )
            item.suffix_stat_boosts["CRIT"] = random.randint(
                0 + difficulty, 50 * difficulty
            )
        item.item_name = item.prefix + " " + item_type + " " + item.suffix
        item.item_description = "ATK: {} +{} +{}\tDEF: {} +{} +{}\nHP: {} +{} +{}\tCRIT: {} +{} +{}".format(
            item.item_stats["ATK"],
            item.prefix_stat_boosts["ATK"],
            item.suffix_stat_boosts["ATK"],
            item.item_stats["DEF"],
            item.prefix_stat_boosts["DEF"],
            item.suffix_stat_boosts["DEF"],
            item.item_stats["HP"],
            item.prefix_stat_boosts["HP"],
            item.suffix_stat_boosts["HP"],
            item.item_stats["CRIT"],
            item.prefix_stat_boosts["CRIT"],
            item.suffix_stat_boosts["CRIT"],
        )
        print(item.item_name)
        print(item.item_description)
        print(item.prefix)
        print(item.suffix)
        return item

    def create_unique(
        self,
        name,
        slot,
        stats={"ATK": 10, "DEF": 10, "HP": 10, "CRIT": 5},
        prefix="",
        prefix_stat_boosts={"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0},
        suffix="",
        suffix_stat_boosts={"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0},
    ) -> RPGItem:
        item = RPGItem()
        item.item_stats = stats
        item.item_slot = slot
        item.item_name = prefix + " " + name + " " + suffix
        item.prefix = prefix
        item.suffix = suffix
        item.prefix_stat_boosts = prefix_stat_boosts
        item.suffix_stat_boosts = suffix_stat_boosts
        item.item_description = "ATK: {} +{} +{}\t\t\tDEF: {} +{} +{}\nHP: {} +{} +{}\t\t\tCRIT: {} +{} +{}".format(
            item.item_stats["ATK"],
            item.prefix_stat_boosts["ATK"],
            item.suffix_stat_boosts["ATK"],
            item.item_stats["DEF"],
            item.prefix_stat_boosts["DEF"],
            item.suffix_stat_boosts["DEF"],
            item.item_stats["HP"],
            item.prefix_stat_boosts["HP"],
            item.suffix_stat_boosts["HP"],
            item.item_stats["CRIT"],
            item.prefix_stat_boosts["CRIT"],
            item.suffix_stat_boosts["CRIT"],
        )
        return item

    def create_from_string(self, istr: str) -> RPGItem:
        split: list = istr.split("|")
        if len(split) > 2:
            item = RPGItem()
            item.item_name = split[0]
            item.item_stats["ATK"] = int(split[1])
            item.item_stats["DEF"] = int(split[2])
            item.item_stats["HP"] = int(split[3])
            item.item_stats["CRIT"] = int(split[4])
            item.item_slot = int(split[5])
            item.prefix = split[6]
            item.prefix_stat_boosts["ATK"] = int(split[7])
            item.prefix_stat_boosts["DEF"] = int(split[8])
            item.prefix_stat_boosts["HP"] = int(split[9])
            item.prefix_stat_boosts["CRIT"] = int(split[10])
            item.suffix = split[11]
            item.suffix_stat_boosts["ATK"] = int(split[12])
            item.suffix_stat_boosts["DEF"] = int(split[13])
            item.suffix_stat_boosts["HP"] = int(split[14])
            item.suffix_stat_boosts["CRIT"] = int(split[15])
            item.item_description = "ATK: {} +{} +{}\t\t\tDEF: {} +{} +{}\nHP: {} +{} +{}\t\t\tCRIT: {} +{} +{}".format(
                item.item_stats["ATK"],
                item.prefix_stat_boosts["ATK"],
                item.suffix_stat_boosts["ATK"],
                item.item_stats["DEF"],
                item.prefix_stat_boosts["DEF"],
                item.suffix_stat_boosts["DEF"],
                item.item_stats["HP"],
                item.prefix_stat_boosts["HP"],
                item.suffix_stat_boosts["HP"],
                item.item_stats["CRIT"],
                item.prefix_stat_boosts["CRIT"],
                item.suffix_stat_boosts["CRIT"],
            )
            return item
        return None


RPG_Level_Requirements: dict = {
    2: 1000,
    3: 1750,
    4: 2500,
    5: 5000,
    6: 7500,
    7: 10000,
    8: 17500,
    9: 30000,
    10: 45000,
    11: 75000,
    12: 150000,
    13: 250000,
    14: 500000,
    15: 750000,
    16: 1000000,
    17: 1250000,
    18: 1500000,
    19: 1750000,
    20: 2000000,
    21: 2500000,
    22: 3000000,
    23: 3500000,
    24: 4000000,
    25: 5000000,
    26: 6000000,
    27: 7000000,
    28: 8000000,
    29: 9000000,
    30: 10000000,
}


class Archetype(Enum):
    Mage = 0  # Extreme Attack / Low Hp / Low Defence / Middle Crit
    Warrior = 1  # Middle Attack / Middle HP / High Defence / Low Crit
    Ranger = 2  # High Attack / Middle HP / Low Defence / High Crit
    Rogue = 3  # High Attack / Low Hp / Low Defence / Extreme Crit
    Priest = 4  # Low Attack / High HP / Middle Defence / Low Crit


class ClassPath(Enum):
    Chaos = 0  # +20% Damage & +25% Crit chance
    Order = 1  # +20% HP & +25% Defence


class MageChaosSpecialization(Enum):
    Fire = 0  # +33% Damage
    Storm = 1  # +33% Crit
    Ice = 2  # +33% Defence


class MageOrderSpecialization(Enum):
    Earth = 0  # +33% Defence
    Nature = 1  # +33% HP
    Moon = 2  # +33% Damage


class MageFireMastery(Enum):
    Blaze = 0  # +50% Damage, +20% Defence & +10% Crit
    Inferno = 1  # +50% Damage & +30% Crit
    Ash = 2  # +50% Damage, +20% Defence & +10% HP
    Lava = 3  # +50% Damage & +30% HP


class MageStormMastery(Enum):
    Thunder = 0
    Tsunami = 1
    Hurricane = 2


class RPGCharacter:
    def __init__(self, owner: int, name: str, archetype: int):
        self.owner = owner
        self.name = name
        self.archetype: int = archetype
        self.path = -1
        self.specialization = -1
        self.mastery = -1
        self.stats: dict = {"ATK": 0, "DEF": 0, "HP": 0, "CRIT": 0}
        self.level: int = 0
        self.xp: int = 0
        self.inventory: list = []
        self.equipment: dict = {"MH": RPGItem(), "OH": RPGItem(), "ARM": RPGItem()}


class RPGCharacterCreator:
    def __init__(self):
        pass

    def create_blank(self, owner: int, name: str, archetype) -> RPGCharacter:
        new_char: RPGCharacter = RPGCharacter(owner, name, archetype)
        new_char.level = 1
        new_char.xp = 0
        new_char.path = -1
        new_char.specialization = -1
        new_char.mastery = -1
        new_char.inventory = []
        if new_char.archetype == 0:
            new_char.stats["ATK"] = 25
            new_char.stats["DEF"] = 5
            new_char.stats["HP"] = 5
            new_char.stats["CRIT"] = 10
        if new_char.archetype == 1:
            new_char.stats["ATK"] = 5
            new_char.stats["DEF"] = 15
            new_char.stats["HP"] = 15
            new_char.stats["CRIT"] = 5
        if new_char.archetype == 2:
            new_char.stats["ATK"] = 15
            new_char.stats["DEF"] = 10
            new_char.stats["HP"] = 10
            new_char.stats["CRIT"] = 10
        if new_char.archetype == 3:
            new_char.stats["ATK"] = 15
            new_char.stats["DEF"] = 5
            new_char.stats["HP"] = 5
            new_char.stats["CRIT"] = 25
        if new_char.archetype == 4:
            new_char.stats["ATK"] = 5
            new_char.stats["DEF"] = 10
            new_char.stats["HP"] = 10
            new_char.stats["CRIT"] = 15
        return new_char


class RPGController:
    def __init__(self):
        self.ItemCreator = RPGItemCreator()
        self.CharacterCreator = RPGCharacterCreator()
        self.characters: list = []
        self.cptr: int = 0
        self.chr_separator = "/"

    def pull(self) -> None:
        global RPGDATA

        line: str = "0000000000000000"
        with open(RPGDATA, "r") as db:
            while line != "":
                try:
                    line = db.readline().rstrip().lstrip()  # check users
                    split: list = line.split(self.chr_separator)
                    if len(split) > 2:
                        char: RPGCharacter = RPGCharacter(split[0], split[1], split[4])
                        char.level = int(split[2])
                        char.xp = int(split[3])
                        char.path = int(split[5])
                        char.specialization = int(split[6])
                        char.mastery = int(split[7])
                        char.stats["ATK"] = int(split[8])
                        char.stats["DEF"] = int(split[9])
                        char.stats["HP"] = int(split[10])
                        char.stats["CRIT"] = int(split[11])
                        MH = self.ItemCreator.create_from_string(split[12])
                        OH = self.ItemCreator.create_from_string(split[13])
                        ARM = self.ItemCreator.create_from_string(split[14])
                        char.inventory = split[15].split(",")
                        char.equipment = {"MH": MH, "OH": OH, "ARM": ARM}
                        self.characters.append(char)
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Pull->Read Character owned by ({})".format(char.owner)
                            + S.RESET_ALL
                        )
                               
                        self.cptr += 1
                except StopIteration:
                    print(
                        "CNDB::Pull->End of file encountered when reading through data stored on disk"
                    )

    def push(self) -> None:
        global RPGDATA

        with open(RPGDATA, "w") as clear:
            clear.write("")
        self.cptr = 0
        line: str = "0000000000000000"
        with open(RPGDATA, "a") as db:
            while line != "" and self.cptr < len(self.characters):
                try:
                    char = self.characters[self.cptr]
                    MH: RPGItem = char.equipment["MH"]
                    OH: RPGItem = char.equipment["OH"]
                    ARM: RPGItem = char.equipment["ARM"]
                    if MH == None or OH == None or ARM == None:
                        print("Empty equipment")
                    if char == None:
                        print("Empty RPG character")
                    else:
                        line = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}\n".format(
                            char.owner,
                            self.chr_separator,
                            char.name,
                            self.chr_separator,
                            char.level,
                            self.chr_separator,
                            char.xp,
                            self.chr_separator,
                            char.archetype,
                            self.chr_separator,
                            char.path,
                            self.chr_separator,
                            char.specialization,
                            self.chr_separator,
                            char.mastery,
                            self.chr_separator,
                            char.stats["ATK"],
                            self.chr_separator,
                            char.stats["DEF"],
                            self.chr_separator,
                            char.stats["HP"],
                            self.chr_separator,
                            char.stats["CRIT"],
                            self.chr_separator,
                            MH.stringify(),
                            self.chr_separator,
                            OH.stringify(),
                            self.chr_separator,
                            ARM.stringify(),
                            self.chr_separator,
                            str(char.inventory),
                        )
                        db.write(line)
                        print(
                            B.BLUE
                            + F.WHITE
                            + "CNDB::Push->Wrote Character registered to ({})".format(
                                self.characters[self.cptr].owner
                            )
                            + S.RESET_ALL
                        )
                    self.cptr += 1
                except StopIteration:
                    print(
                        "CNDB::Push->End of file encountered when writing data to disk"
                    )

    def NewCharacter(self, owner: discord.User, name, archetype):
        userid: str = str(owner.id)
        for char in self.characters:
            if char.owner == userid:
                return None
        new_char: RPGCharacter = self.CharacterCreator.create_blank(
            userid, name, archetype
        )
        self.characters.append(new_char)
        self.cptr += 1
        StarterWeapon: RPGItem = RPGItem()
        StarterOffhand: RPGItem = RPGItem()
        StarterArmor: RPGItem = RPGItem()
        if new_char.archetype == 0:
            StarterWeapon = self.ItemCreator.create_unique(
                "Starter Staff", 0, {"ATK": 20, "DEF": 0, "HP": 0, "CRIT": 10}
            )
            StarterOffhand = self.ItemCreator.create_unique(
                "Starter Orb", 1, {"ATK": 20, "DEF": 5, "HP": 10, "CRIT": 20}
            )
            StarterArmor = self.ItemCreator.create_unique(
                "Starter Robe", 2, {"ATK": 0, "DEF": 10, "HP": 10, "CRIT": 0}
            )
        if new_char.archetype == 1:
            StarterWeapon = self.ItemCreator.create_unique(
                "Starter Sword", 0, {"ATK": 10, "DEF": 0, "HP": 0, "CRIT": 10}
            )
            StarterOffhand = self.ItemCreator.create_unique(
                "Starter Shield", 1, {"ATK": 10, "DEF": 25, "HP": 30, "CRIT": 5}
            )
            StarterArmor = self.ItemCreator.create_unique(
                "Starter Plate Armor", 2, {"ATK": 0, "DEF": 40, "HP": 20, "CRIT": 0}
            )
        if new_char.archetype == 2:
            StarterWeapon = self.ItemCreator.create_unique(
                "Starter Bow", 0, {"ATK": 20, "DEF": 0, "HP": 0, "CRIT": 15}
            )
            StarterOffhand = self.ItemCreator.create_unique(
                "Starter Shield", 1, {"ATK": 20, "DEF": 15, "HP": 10, "CRIT": 20}
            )
            StarterArmor = self.ItemCreator.create_unique(
                "Starter Leather Armor", 2, {"ATK": 0, "DEF": 15, "HP": 15, "CRIT": 0}
            )
        if new_char.archetype == 3:
            StarterWeapon = self.ItemCreator.create_unique(
                "Starter Sword", 0, {"ATK": 5, "DEF": 0, "HP": 0, "CRIT": 40}
            )
            StarterOffhand = self.ItemCreator.create_unique(
                "Starter Shield", 1, {"ATK": 5, "DEF": 5, "HP": 10, "CRIT": 30}
            )
            StarterArmor = self.ItemCreator.create_unique(
                "Starter Leather Armor", 2, {"ATK": 0, "DEF": 10, "HP": 10, "CRIT": 0}
            )
        if new_char.archetype == 4:
            StarterWeapon = self.ItemCreator.create_unique(
                "Starter Mace", 0, {"ATK": 10, "DEF": 0, "HP": 0, "CRIT": 10}
            )
            StarterOffhand = self.ItemCreator.create_unique(
                "Starter Book", 1, {"ATK": 10, "DEF": 25, "HP": 20, "CRIT": 10}
            )
            StarterArmor = self.ItemCreator.create_unique(
                "Starter Robe", 2, {"ATK": 0, "DEF": 20, "HP": 20, "CRIT": 0}
            )
        new_char.equipment = {
            "MH": StarterWeapon,
            "OH": StarterOffhand,
            "ARM": StarterArmor,
        }
        return -1
