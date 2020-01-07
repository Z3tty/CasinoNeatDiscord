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
import json

Prefixes: list = ["Divine", "Hellish", "Enormous", "Gigantic", "Colossal", "Tiny", "Miniscule", "Bright", "Dark", "Honed", "Sharpened", "Ruiner's"]
Suffixes: list = ["of Terror", "of the Skies", "of Gaia", "of the Slayer", "of Legend", "of Storms", "of Hellflame", "of the Hunter", "of the Reaper"]
WeaponTypes: list = ["Sword", "Spear", "Glaive", "Axe", "Mace", "Staff", "Dagger", "Shortsword", "Rapier", "Hammer", "Bow", "Wand", "Orb", "Twinblade", "Grimoire", "Pike", "Greatsword", "Halberd"]
ArmorTypes: list = ["Hide Armor", "Steel Armor", "Obsidian Armor", "Plated Armor", "Fur Armor", "Winged Armor", "Magma Armor"]
Bosses: dict = {
        0:"Moo, the Cow",
        10:"Aatraloc the Damned",
        20:"Bercial the Hollow",
        30:"Maptabat the Forsaken",
        40:"Kuhg the Beast",
        50:"Hagayu the Lost",
        60:"Brahamiz the Storm",
        70:"Kharzargaet of the Deep Seas",
        80:"Jeex the Unyielding",
        90:"Veztrec of Hellflame",
        100:"Fuuree the Scourge"
}

Raids: dict = {
    "Graax" : "of Devouring",
    "Halyz" : "of the Void",
    "Penembrum" : "of the Umbral Deep",
    "Olicarn" : "of Song and Dance",
    "Azzidem" : "of Corruption"
}

class Generator:
    def __init__(self):
        pass

    def random_item(self, luck_boost: int) -> dict:
        item:dict = {
            "name":"",
            "rarity":"",
            "ATK":"",
            "DEF":"",
            "LUCK":"",
        }
        is_weapon: bool = random.randint(0, 10) < 5
        has_prefix: bool = random.randint(0, 100) - luck_boost < 10
        has_suffix: bool = random.randint(0, 100) - luck_boost < 5
        rarity_roll: int = random.randint(0, 65536) - luck_boost
        if is_weapon:
            item["type"] = "WPN"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(WeaponTypes) + " ",
                random.choice(Suffixes) if has_suffix else ""
            )
            if rarity_roll < 50000:
                item["rarity"] = "Uncommon"
                item["ATK"] = str(random.randint(150, 500))
                item["DEF"] = str(random.randint(15, 50))
                item["LUCK"] = str(random.randint(0, 250))
            if rarity_roll < 10000:
                item["rarity"] = "Rare"
                item["ATK"] = str(random.randint(600, 2000))
                item["DEF"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(0, 500))
            if rarity_roll < 255:
                item["rarity"] = "Epic"
                item["ATK"] = str(random.randint(1000, 5000))
                item["DEF"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(0, 750))
            if rarity_roll < 35:
                item["rarity"] = "Legendary"
                item["ATK"] = str(random.randint(6000, 10000))
                item["DEF"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(0, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["ATK"] = str(random.randint(15000, 50000))
                item["DEF"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(0, 5000))
            if rarity_roll > 50000:
                item["rarity"] = "Common"
                item["ATK"] = str(random.randint(10, 200))
                item["DEF"] = str(random.randint(10, 20))
                item["LUCK"] = str(random.randint(0, 25))
        else:
            item["type"] = "ARM"
            item["name"] = "{}{}{}".format(
                random.choice(Prefixes) + " " if has_prefix else "",
                random.choice(ArmorTypes) + " ",
                random.choice(Suffixes) if has_suffix else ""
            )
            if rarity_roll < 50000:
                item["rarity"] = "Uncommon"
                item["DEF"] = str(random.randint(150, 500))
                item["ATK"] = str(random.randint(15, 50))
                item["LUCK"] = str(random.randint(0, 250))
            if rarity_roll < 10000:
                item["rarity"] = "Rare"
                item["DEF"] = str(random.randint(600, 2000))
                item["ATK"] = str(random.randint(60, 200))
                item["LUCK"] = str(random.randint(0, 500))
            if rarity_roll < 255:
                item["rarity"] = "Epic"
                item["DEF"] = str(random.randint(1000, 5000))
                item["ATK"] = str(random.randint(100, 500))
                item["LUCK"] = str(random.randint(0, 750))
            if rarity_roll < 35:
                item["rarity"] = "Legendary"
                item["DEF"] = str(random.randint(6000, 10000))
                item["ATK"] = str(random.randint(600, 1000))
                item["LUCK"] = str(random.randint(0, 1000))
            if rarity_roll < 5:
                item["rarity"] = "Artifact"
                item["DEF"] = str(random.randint(15000, 50000))
                item["ATK"] = str(random.randint(1500, 5000))
                item["LUCK"] = str(random.randint(0, 5000))
            if rarity_roll > 50000:
                item["rarity"] = "Common"
                item["DEF"] = str(random.randint(10, 200))
                item["ATK"] = str(random.randint(10, 20))
                item["LUCK"] = str(random.randint(0, 25))
                
        
        return item
    
    def generate_boss(self, dungeon: int) -> dict:
        if dungeon > 10: return {None: None}
        if dungeon == 0:
            boss: dict = {
                "name":Bosses[0],
                "ATK":"5",
                "DEF":"5"
            }
            return boss
        boss : dict = {
            "name":Bosses[(dungeon * 10)],
            "ATK": str(dungeon * 150 + (dungeon - 1) * 1000),
            "DEF": str(dungeon * 150 + (dungeon - 1) * 1000),
        }
        if dungeon > 4:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 2000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 2000)
        if dungeon > 6:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 3000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 3000)
        if dungeon > 8:
            boss["ATK"] = str(int(boss["ATK"]) + dungeon * 4000)
            boss["DEF"] = str(int(boss["DEF"]) + dungeon * 4000)
        return boss
    
    def generate_raid_boss(self) -> dict:
        boss: int = random.randint(0, 4)
        BossInfo = {
            "name": "",
            "suffix": "",
            "ATK": "",
            "DEF": "",
        }
        RaidAttack = 400000
        RaidDefense = 400000
        if boss == 0:
            BossInfo["name"] = "Graax"
            BossInfo["suffix"] = Raids["Graax"]
        if boss == 1:
            BossInfo["name"] = "Halyz"
            BossInfo["suffix"] = Raids["Halyz"]
        if boss == 2:
            BossInfo["name"] = "Penembrum"
            BossInfo["suffix"] = Raids["Penembrum"]
        if boss == 3:
            BossInfo["name"] = "Olicarn"
            BossInfo["suffix"] = Raids["Olicarn"]
        if boss == 4:
            BossInfo["name"] = "Azzidem"
            BossInfo["suffix"] = Raids["Azzidem"]
        BossInfo["ATK"] = str(random.randint(RaidAttack, int(RaidAttack * 1.7)))
        BossInfo["DEF"] = str(random.randint(RaidDefense, int(RaidDefense * 1.7)))
        return BossInfo
