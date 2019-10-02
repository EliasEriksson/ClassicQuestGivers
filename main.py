from typing import List
from ClassicQuestGivers.ClassicQuestGivers.manager import Manager
from ClassicQuestGivers.ClassicQuestGivers.db import Quest
from slpp import slpp
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


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("character", type=str, help="Your characters name.")
    parser.add_argument("realm", type=str, help="Your characters realm.")
    parser.add_argument("faction", type=str, help="H N A")
    parser.add_argument("--zone", type=str, help="Name of the zones to search.")
    parser.add_argument("--levels_higher", type=int, help="Ammount of levels above you.")
    parser.add_argument("--levels_lower", type=int, help="Ammount of levels bellow you.")

    args = parser.parse_args()
    path = Path(load_json("settings.json")["wow_path"])
    path = path.joinpath("_classic_/WTF/Account/101169538#2/SavedVariables/+Wowhead_Looter.lua")
    profile = lua(path)
    character = profile["^".join((args.character.capitalize(), args.realm.capitalize()))]

    level = character["level"]
    faction = args.faction if args.faction else "N"
    higher = args.levels_higher if args.levels_higher else 2
    lower = args.levels_lower if args.levels_lower else 2
    zone = args.zone if args.zone else None

    with Manager() as cursor:
        quests: List[Quest] = cursor.get_quest(level, faction, higher, lower, zone)
    for quest in quests:
        if quest.id not in character["quests"]:
            printf(format_quest(quest))


def lua(path: Path) -> dict:
    content = path.read_text()
    match = re.search(r"wlProfileData\s=\s({.*},\n})\n", content, re.DOTALL)
    if match:
        d = slpp.decode(match.groups()[0])
        return d
    raise SyntaxError


if __name__ == '__main__':
    parse()
