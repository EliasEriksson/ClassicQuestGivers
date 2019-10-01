from typing import List


def build_urls(filename: str) -> List[str]:
    base = "https://classic.wowhead.com/"
    with open(filename) as f:
        return [base + zone.lower().replace(" ", "-").strip() + "#quests"
                for zone in f]


if __name__ == '__main__':
    print(build_urls("zones.txt"))
