from typing import List
from ClassicQuestGivers.ClassicQuestGivers.manager import Manager
from ClassicQuestGivers.ClassicQuestGivers.db import Quest
from slpp import slpp
from pathlib import Path
import argparse
import os
import re


def hyper(link, text):
    return f"\e]8;;{link}\e\\\\{text}\e]8;;\e\\\\"


def format_quests(quests: List[Quest]) -> List[str]:
    # Availeble quest ´questname´ from `npc`, req level `level` recomended level `level`
    formated = [
        f"Availeble quest {hyper(quest.link, quest.name)} from {hyper(quest.npc_link, quest.npc)} in {quest.zone}.\n"
        f"Recomended level {quest.level} requires {quest.req}."
        for quest in quests]

    return formated


def printf(text: str):
    os.system(f'printf "{text}\n\n"')


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("level", type=int, help="Your level.")
    parser.add_argument("faction", type=str, help="H N A")
    parser.add_argument("--zone", type=str, help="Name of the zones to search.")
    parser.add_argument("--levels_hihger", type=int, help="Ammount of levels above you.")
    parser.add_argument("--levels_lower", type=int, help="Ammount of levels bellow you.")

    args = parser.parse_args()
    faction = args.faction if args.faction else "N"
    higher = args.levels_hihger if args.levels_hihger else 2
    lower = args.levels_lower if args.levels_lower else 2
    zone = args.zone if args.zone else None

    with Manager() as cursor:
        quests = cursor.get_quest(args.level, faction, higher, lower, zone)
        quests = format_quests(quests)
        for quest in quests:
            printf(quest)


def lua(filename: str):
    content = Path(filename).read_text()
    match = re.search(r"wlProfileData = {.*\}", content)
    print(match)

    # print(content)
    # # with open(filename) as f:
    # d = slpp.decode(content)
    # print(d[list(d.keys())[0]]["quests"])


if __name__ == '__main__':
    lua("Wowhead_Looter.lua")
