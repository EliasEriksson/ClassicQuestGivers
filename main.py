from typing import List
from ClassicQuestGivers.ClassicQuestGivers.manager import Manager
from ClassicQuestGivers.ClassicQuestGivers.db import Quest
from slpp import slpp as lua
from pathlib import Path
import argparse
import os
import re
import json


def hyper(link, text):
    return f"\e]8;;{link}\e\\\\{text}\e]8;;\e\\\\"


def load_json(filename: str):
    with open(filename) as f:
        return json.load(f)


def format_quest(quest: Quest) -> str:
    return f"Availeble quest {hyper(quest.link, quest.name)} from " \
           f"{hyper(quest.npc_link, quest.npc)} in {quest.zone}.\n" \
           f"Recomended level {quest.level} requires {quest.req}."


def printf(text: str):
    os.system(f'printf "{text}\n\n"')


def get_wl_profile(path: Path) -> dict:
    content = path.read_text()
    match = re.search(r"wlProfile\s=\s({.*},\n})\n", content, re.DOTALL)
    if match:
        var = lua.decode(match.groups()[0])
        return var


def get_wl_profile_data(path: Path) -> dict:
    content = path.read_text()
    match = re.search(r"wlProfileData\s=\s({.*},\n})\n", content, re.DOTALL)
    if match:
        var = lua.decode(match.groups()[0])
        return var


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("character", type=str, help="Your characters name.")
    parser.add_argument("realm", type=str, help="Your characters realm.")
    parser.add_argument("--zone", type=str, help="Name of the zones to search.")
    parser.add_argument("--levels_higher", type=int, help="Ammount of levels above you.")
    parser.add_argument("--levels_lower", type=int, help="Ammount of levels bellow you.")
    parser.add_argument("--faction", type=str, help="H N A")
    parser.add_argument("--file", type=str, help="Full path to '+Wowhead_Looter.lua' file.")

    args = parser.parse_args()
    if args.file:
        path = Path(args.file)
    else:
        path = Path(load_json("settings.json")["wow_path"])
        path = path.joinpath("_classic_/WTF/Account/101169538#2/SavedVariables/+Wowhead_Looter.lua")

    profile = get_wl_profile(path)
    profile_data = get_wl_profile_data(path)
    character = "^".join((args.character.capitalize(), args.realm.capitalize()))

    level = profile_data[character]["level"]
    faction = args.faction if args.faction else profile[character]["faction"][0].upper() + "N"
    higher = args.levels_higher if args.levels_higher else 2
    lower = args.levels_lower if args.levels_lower else 2
    zone = args.zone if args.zone else None

    with Manager() as cursor:
        quests: List[Quest] = cursor.get_quest(level, faction, higher, lower, zone)
    for quest in quests:
        if quest.id not in profile_data[character]["quests"]:
            printf(format_quest(quest))


if __name__ == '__main__':
    parse()
