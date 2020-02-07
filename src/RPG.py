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
import discord
import random
from colorama import init

init()
from colorama import Fore as F
from colorama import Style as S
from colorama import Back as B
from enum import Enum
import json

Prefixes: list = [
    "Divine",
    "Hellish",
    "Fine",
    "Superb",
    "Angelic",
    "Legendary",
    "Voidtouched",
    "Bright",
    "Dark",
    "Honed",
    "Sharpened",
    "Ruiner's",
]
Suffixes: list = [
    "of Terror",
    "of the Skies",
    "of Gaia",
    "of the Slayer",
    "of Legend",
    "of Storms",
    "of Hellflame",
    "of the Hunter",
    "of the Reaper",
]
UniquePrefixes: list = ["Heroic", "Perfect", "Cosmic", "Ascended", "Ancient"]
UniqueSuffixes: list = [
    "of Evisceration",
    "of Obliteration",
    "of Decimation",
    "of the God-Slayer",
    "of the Dominator",
]
WeaponTypes: list = [
    "Sword",
    "Spear",
    "Glaive",
    "Axe",
    "Mace",
    "Staff",
    "Dagger",
    "Shortsword",
    "Rapier",
    "Hammer",
    "Bow",
    "Wand",
    "Orb",
    "Twinblade",
    "Grimoire",
    "Pike",
    "Greatsword",
    "Halberd",
]
ArmorTypes: list = [
    "Hide Armor",
    "Steel Armor",
    "Obsidian Armor",
    "Plated Armor",
    "Fur Armor",
    "Winged Armor",
    "Magma Armor",
]
RingTypes: list = [
    "Silver Ring",
    "Gold Ring",
    "Diamond Ring",
    "Wooden Ring",
    "Crystal Ring",
    "Bronze Ring",
    "Brass Ring",
    "Platinum Ring",
]
NeckTypes: list = [
    "Velvet Cape",
    "Studded Cape",
    "Inlaid Cape",
    "Brass Necklace",
    "Brass Amulet",
    "Gold Necklace",
    "Gold Amulet",
    "Silver Necklace",
    "Silver Amulet",
    "Platinum Necklace",
    "Platinum Amulet",
    "Crystal Necklace",
    "Crystal Amulet",
]
AccTypes: list = ["Hat", "Shoes", "Gloves", "Belt"]
Bosses: dict = {
    0: "Moo, the Cow",
    1: "Aatraloc the Damned",
    2: "Bercial the Hollow",
    3: "Maptabat the Forsaken",
    4: "Kuhg the Beast",
    5: "Hagayu the Lost",
    6: "Brahamiz the Storm",
    7: "Kharzargaet of the Deep Seas",
    8: "Jeex the Unyielding",
    9: "Veztrec of Hellflame",
    10: "Fuuree the Scourge",
    11: "Baliel of the Dying Star",
    12: "Petrax the Decieved",
    13: "Puppet of Azzidem",
    14: "Congregation of Olicarn",
    15: "Beastmaster Oka",
    16: "Umbral General Xee",
    17: "Laine of the Burning Planes",
    18: "Aptabus of the Neverending Wheel",
    19: "Permafrost Dragon Vimia",
    20: "Za'lem, Lord of the Cosmos",
}

Raids: dict = {
    "Graax": "of Devouring",
    "Halyz": "of the Void",
    "Penembrum": "of the Umbral Deep",
    "Olicarn": "of Song and Dance",
    "Azzidem": "of Corruption",
    "Zadr": "the Solemn Primordial",
}


class Generator:
    def __init__(self):
        pass

    def random_item(self, luck_boost: int, isRaid: bool = False) -> dict:
        item: dict = {"name": "", "rarity": "", "ATK": "", "DEF": "", "LUCK": ""}
        type_roll = random.randint(0, 4)
        has_prefix: bool = random.randint(0, 100) - luck_boost < 10
        has_suffix: bool = random.randint(0, 100) - luck_boost < 5
        rarity_roll: int = random.randint(0, 1000000) - luck_boost
        if type_roll == 0:
            item["type"] = "WPN"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(WeaponTypes) + " ",
                random.choice(Suffixes) if has_suffix else "",
            )
            if isRaid:
                if random.randint(0, 100000) - luck_boost <= 0:
                    item["rarity"] = "Relic"
                    item["ATK"] = str(random.randint(50000, 100000))
                    item["DEF"] = str(random.randint(5000, 10000))
                    item["LUCK"] = str(random.randint(1000, 25000))
                    return item
            if rarity_roll < 950000:
                item["rarity"] = "Uncommon"
                item["ATK"] = str(random.randint(150, 500))
                item["DEF"] = str(random.randint(15, 50))
                item["LUCK"] = str(random.randint(0, 250))
            if rarity_roll < 800000:
                item["rarity"] = "Rare"
                item["ATK"] = str(random.randint(600, 2000))
                item["DEF"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(0, 500))
            if rarity_roll < 100000:
                item["rarity"] = "Epic"
                item["ATK"] = str(random.randint(1000, 5000))
                item["DEF"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(0, 750))
            if rarity_roll < 5000:
                item["rarity"] = "Legendary"
                item["ATK"] = str(random.randint(6000, 10000))
                item["DEF"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(0, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["ATK"] = str(random.randint(15000, 50000))
                item["DEF"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(0, 5000))
            if rarity_roll > 950000:
                item["rarity"] = "Common"
                item["ATK"] = str(random.randint(10, 200))
                item["DEF"] = str(random.randint(10, 20))
                item["LUCK"] = str(random.randint(0, 25))
        if type_roll == 1:
            item["type"] = "ARM"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(ArmorTypes) + " ",
                random.choice(Suffixes) if has_suffix else "",
            )
            if isRaid:
                if random.randint(0, 100000) - luck_boost <= 0:
                    item["rarity"] = "Relic"
                    item["ATK"] = str(random.randint(5000, 10000))
                    item["DEF"] = str(random.randint(50000, 100000))
                    item["LUCK"] = str(random.randint(1000, 25000))
                    return item
            if rarity_roll < 950000:
                item["rarity"] = "Uncommon"
                item["DEF"] = str(random.randint(150, 500))
                item["ATK"] = str(random.randint(15, 50))
                item["LUCK"] = str(random.randint(0, 250))
            if rarity_roll < 800000:
                item["rarity"] = "Rare"
                item["DEF"] = str(random.randint(600, 2000))
                item["ATK"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(0, 500))
            if rarity_roll < 100000:
                item["rarity"] = "Epic"
                item["DEF"] = str(random.randint(1000, 5000))
                item["ATK"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(0, 750))
            if rarity_roll < 5000:
                item["rarity"] = "Legendary"
                item["DEF"] = str(random.randint(6000, 10000))
                item["ATK"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(0, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["DEF"] = str(random.randint(15000, 50000))
                item["ATK"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(0, 5000))
            if rarity_roll > 950000:
                item["rarity"] = "Common"
                item["DEF"] = str(random.randint(10, 200))
                item["ATK"] = str(random.randint(10, 20))
                item["LUCK"] = str(random.randint(0, 25))
        if type_roll == 2:
            item["type"] = "RNG"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(RingTypes) + " ",
                random.choice(Suffixes) if has_suffix else "",
            )
            if isRaid:
                if random.randint(0, 100000) - luck_boost <= 0:
                    item["rarity"] = "Relic"
                    item["ATK"] = str(random.randint(5000, 10000))
                    item["DEF"] = str(random.randint(5000, 10000))
                    item["LUCK"] = str(random.randint(20000, 50000))
                    return item
            if rarity_roll < 950000:
                item["rarity"] = "Uncommon"
                item["ATK"] = str(random.randint(10, 50))
                item["DEF"] = str(random.randint(10, 50))
                item["LUCK"] = str(random.randint(50, 250))
            if rarity_roll < 800000:
                item["rarity"] = "Rare"
                item["ATK"] = str(random.randint(60, 200))
                item["DEF"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(400, 600))
            if rarity_roll < 100000:
                item["rarity"] = "Epic"
                item["ATK"] = str(random.randint(100, 500))
                item["DEF"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(1000, 5000))
            if rarity_roll < 5000:
                item["rarity"] = "Legendary"
                item["ATK"] = str(random.randint(600, 1000))
                item["DEF"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(5000, 10000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["ATK"] = str(random.randint(1500, 5000))
                item["DEF"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(10000, 20000))
            if rarity_roll > 950000:
                item["rarity"] = "Common"
                item["ATK"] = "0"
                item["DEF"] = "0"
                item["LUCK"] = str(random.randint(5, 25))
        if type_roll == 3:
            item["type"] = "NCK"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(NeckTypes) + " ",
                random.choice(Suffixes) if has_suffix else "",
            )
            if isRaid:
                if random.randint(0, 100000) - luck_boost <= 0:
                    item["rarity"] = "Relic"
                    item["ATK"] = str(random.randint(5000, 10000))
                    item["DEF"] = str(random.randint(5000, 10000))
                    item["LUCK"] = str(random.randint(5000, 10000))
                    return item
            if rarity_roll < 950000:
                item["rarity"] = "Uncommon"
                item["ATK"] = str(random.randint(10, 50))
                item["DEF"] = str(random.randint(10, 50))
                item["LUCK"] = str(random.randint(10, 50))
            if rarity_roll < 800000:
                item["rarity"] = "Rare"
                item["ATK"] = str(random.randint(60, 200))
                item["DEF"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(60, 200))
            if rarity_roll < 100000:
                item["rarity"] = "Epic"
                item["ATK"] = str(random.randint(100, 500))
                item["DEF"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(100, 500))
            if rarity_roll < 5000:
                item["rarity"] = "Legendary"
                item["ATK"] = str(random.randint(600, 1000))
                item["DEF"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(600, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["ATK"] = str(random.randint(1500, 5000))
                item["DEF"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(1500, 5000))
            if rarity_roll > 950000:
                item["rarity"] = "Common"
                item["ATK"] = str(random.randint(5, 25))
                item["DEF"] = str(random.randint(5, 25))
                item["LUCK"] = str(random.randint(5, 25))
        if type_roll == 4:
            item["type"] = "ACC"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(AccTypes) + " ",
                random.choice(Suffixes) if has_suffix else "",
            )
            if isRaid:
                if random.randint(0, 100000) - luck_boost <= 0:
                    item["rarity"] = "Relic"
                    item["ATK"] = str(random.randint(5000, 10000))
                    item["DEF"] = str(random.randint(5000, 10000))
                    item["LUCK"] = str(random.randint(5000, 10000))
                    return item
            if rarity_roll < 950000:
                item["rarity"] = "Uncommon"
                item["ATK"] = str(random.randint(10, 50))
                item["DEF"] = str(random.randint(10, 50))
                item["LUCK"] = str(random.randint(10, 50))
            if rarity_roll < 800000:
                item["rarity"] = "Rare"
                item["ATK"] = str(random.randint(60, 200))
                item["DEF"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(60, 200))
            if rarity_roll < 100000:
                item["rarity"] = "Epic"
                item["ATK"] = str(random.randint(100, 500))
                item["DEF"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(100, 500))
            if rarity_roll < 5000:
                item["rarity"] = "Legendary"
                item["ATK"] = str(random.randint(600, 1000))
                item["DEF"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(600, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["ATK"] = str(random.randint(1500, 5000))
                item["DEF"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(1500, 5000))
            if rarity_roll > 950000:
                item["rarity"] = "Common"
                item["ATK"] = str(random.randint(5, 25))
                item["DEF"] = str(random.randint(5, 25))
                item["LUCK"] = str(random.randint(5, 25))
        return item

    def generate_boss(self, dungeon: int) -> dict:
        if dungeon > 20 or dungeon < 0:
            return {None: None}
        if dungeon == 0:
            boss: dict = {"name": Bosses[0], "ATK": "5", "DEF": "5"}
            return boss
        boss: dict = {
            "name": Bosses[dungeon],
            "ATK": str(dungeon * 150 + (dungeon - 1) * 1000),
            "DEF": str(dungeon * 150 + (dungeon - 1) * 1000),
        }
        if dungeon < 5:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 2000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 2000)
        elif dungeon < 7:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 3000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 3000)
        elif dungeon < 9:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 4000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 4000)
        elif dungeon < 13:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 5000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 5000)
        elif dungeon < 15:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 10000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 10000)
        elif dungeon < 17:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 15000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 15000)
        elif dungeon < 21:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 25000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 25000)
        return boss

    def generate_raid_boss(self) -> dict:
        boss: int = random.randint(0, 4)
        BossInfo = {"name": "", "suffix": "", "ATK": "", "DEF": ""}
        RaidAttack = 600000
        RaidDefense = 600000
        if boss == 0:
            BossInfo["name"] = "Graax"
        if boss == 1:
            BossInfo["name"] = "Halyz"
        if boss == 2:
            BossInfo["name"] = "Penembrum"
        if boss == 3:
            BossInfo["name"] = "Olicarn"
        if boss == 4:
            BossInfo["name"] = "Azzidem"
        BossInfo["suffix"] = Raids[BossInfo["name"]]
        BossInfo["ATK"] = str(random.randint(RaidAttack, int(RaidAttack * 1.7)))
        BossInfo["DEF"] = str(random.randint(RaidDefense, int(RaidDefense * 1.7)))
        return BossInfo

    def make_unique_item(self, name, itemtype, atk, defn, luck) -> dict:
        item: dict = {
            "name": name,
            "type": itemtype,
            "rarity": "Unique",
            "ATK": atk,
            "DEF": defn,
            "LUCK": luck,
        }
        return item

    def forge_item(self, mtype) -> dict:
        item_sigs: dict = {"alpha": "α", "beta": "β", "gamma": "γ"}
        signature: str = item_sigs[mtype]
        item_type_rng: int = random.randint(0, 4)
        item_name: str = "{} ".format(signature)
        item_type: str = ""
        ItemATK: int = 0
        ItemDEF: int = 0
        ItemLCK: int = 0
        StatModifier: int = 1 if mtype == "alpha" else 2 if mtype == "beta" else 3 if mtype == "gamma" else 0
        if item_type_rng == 0:
            item_type = "WPN"
            item_name = "{} {} {} {}".format(
                item_name,
                random.choice(UniquePrefixes),
                random.choice(WeaponTypes),
                random.choice(UniqueSuffixes),
            )
            ItemATK = random.randint(100000 * StatModifier, 200000 * StatModifier)
            ItemDEF = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemLCK = random.randint(50000 * StatModifier, 100000 * StatModifier)
        if item_type_rng == 1:
            item_type = "ARM"
            item_name = "{} {} {} {}".format(
                item_name,
                random.choice(UniquePrefixes),
                random.choice(ArmorTypes),
                random.choice(UniqueSuffixes),
            )
            ItemDEF = random.randint(100000 * StatModifier, 200000 * StatModifier)
            ItemATK = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemLCK = random.randint(50000 * StatModifier, 100000 * StatModifier)
        if item_type_rng == 2:
            item_type = "RNG"
            item_name = "{} {} {} {}".format(
                item_name,
                random.choice(UniquePrefixes),
                random.choice(RingTypes),
                random.choice(UniqueSuffixes),
            )
            ItemLCK = random.randint(100000 * StatModifier, 200000 * StatModifier)
            ItemATK = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemDEF = random.randint(50000 * StatModifier, 100000 * StatModifier)
        if item_type_rng == 3:
            item_type = "NCK"
            item_name = "{} {} {} {}".format(
                item_name,
                random.choice(UniquePrefixes),
                random.choice(NeckTypes),
                random.choice(UniqueSuffixes),
            )
            ItemATK = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemDEF = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemLCK = random.randint(50000 * StatModifier, 100000 * StatModifier)
        if item_type_rng == 4:
            item_type = "ACC"
            item_name = "{} {} {} {}".format(
                item_name,
                random.choice(UniquePrefixes),
                random.choice(AccTypes),
                random.choice(UniqueSuffixes),
            )
            ItemATK = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemDEF = random.randint(50000 * StatModifier, 100000 * StatModifier)
            ItemLCK = random.randint(50000 * StatModifier, 100000 * StatModifier)
        item: dict = {
            "name": item_name,
            "type": item_type,
            "rarity": "Unique",
            "ATK": ItemATK,
            "DEF": ItemDEF,
            "LUCK": ItemLCK,
        }
        return item
