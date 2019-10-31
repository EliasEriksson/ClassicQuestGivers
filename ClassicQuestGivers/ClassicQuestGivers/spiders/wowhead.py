from typing import List
from pathlib import Path
from scrapy import Spider
from scrapy.selector.unified import Selector
from scrapy_splash import SplashResponse
from ..items import Quest
import scrapy_splash
from .. import PROJECT_ROOT


class ZoneSpider(Spider):
    # TODO test parse for class
    # TODO parse for dungeon / pvp / raid tags
    # TODO add class field in database
    name = "wowhead"
    base_url = "https://classic.wowhead.com"

    def format_zone_url(self, zone: str):
        zone = zone.lower().replace(" ", "-").replace("'", "").strip()
        url = f"{self.base_url}/{zone}#quests"
        return url

    def build_urls(self) -> List[str]:
        """
        builds the start urls based on the names in zones.txt in the project root

        :return: urls
        """
        path = Path(PROJECT_ROOT).joinpath("zones.txt")
        with open(str(path)) as zones:
            urls = [self.format_zone_url(zone) for zone in zones]
        return urls

    def start_requests(self):
        """
        initial requests for the crawler

        :return:
        """
        urls = self.build_urls()

        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse_zone)

    def parse_zone(self, response: SplashResponse):
        """
        parses a wowhead zone page

        gathers quest name, link to the quest, quest id, zone name, recomended level and required level
        from the page. then proceedes to do a followup request on each quest in the zone.

        :param response: splash rendered http response
        :return:
        """
        elements: List[Selector] = response.xpath('//*[@id="tab-quests"]/div[2]/table/tbody/tr')

        for element in elements:
            quest = Quest()
            quest["name"] = element.xpath("td[2]/div/a/text()").get()
            quest["link"] = self.base_url + element.xpath("td[2]/div/a/@href").get()
            quest["id"] = int(quest["link"].split("=")[-1].split("/")[0])
            quest["zone"] = response.url.split("/")[-1].split("#")[0]

            level = element.xpath("td[3]/text()").get()
            quest["level"] = int(level) if level else -1

            req = element.xpath("td[4]/text()").get()
            quest["req"] = int(req) if req else -1

            faction = element.xpath("td[5]/span/@class").get()
            if faction:
                if "horde" in faction:
                    quest["faction"] = "H"
                elif "alliance" in faction:
                    quest["faction"] = "A"
                else:
                    quest["faction"] = "N"
            else:
                quest["faction"] = "N"

            yield scrapy_splash.SplashRequest(url=quest["link"], callback=self.parse_quest, meta={"quest": quest})

    def parse_quest(self, response: SplashResponse):
        """
        parses a wowhead quest page

        passes the "quick facts" secton of the page to be parsed by 'parse_quick_facts'
        :param response: splash rendered http response
        :return:
        """

        quest = response.meta.get("quest")
        infobox: Selector = response.xpath('//*[@id="infobox-alternate-position"]/table')

        self.parse_quick_facts(infobox.xpath('//th[@id="infobox-quick-facts"]/../../tr/td/div/ul/li'), quest)

        self.parse_series(infobox.xpath('//th[@id="infobox-series"]/../../tr/td//table[@class="series"]/tbody'), quest)

        self.parse_requirements(infobox.xpath('//th[@id="infobox-requires"]/../../tr/td/div/a'), quest)
        yield quest

    def parse_quick_facts(self, selector: Selector, quest: Quest):
        """
        parses a wowhead quests quick facts section

        extracts npc name, npc link and if the quest is repeatable or not
        :param selector: selection of the quick facts section
        :param quest: quest object to store gathered info in
        :return:
        """
        npc_a_tag = selector.xpath('div/span[contains(text(), "Start:")]/a')
        npc = npc_a_tag.xpath('text()').get()
        npc_link = npc_a_tag.xpath('@href').get()
        class_ = selector.xpath('div[contains(text(), "Class: ")]/a/span/text()')

        quest["npc"] = npc if npc else "Unknown"
        quest["npc_link"] = self.base_url + npc_link if npc_link else "Unknown"
        quest["repeatable"] = True if selector.xpath('div[contains(text(), "Repeatable")]/text()') else False
        quest["class"] = class_ if class_ else "None"

    def parse_series(self, selector: Selector, quest: Quest):
        """
        parses a wowhead quests series section

        extracts a quests id from a previously required quest via series
        and adds a requirement to the quest object
        :param selector: selection of the series section
        :param quest: quest object to store gathered info in
        :return:
        """
        if selector:
            # if its a chain quest
            if selector.xpath('tr/th[contains(text(), "1.")]/../td/div/b'):
                # current quest is the first in series, no series requirements
                pass
            elif selector.xpath('tr/th[contains(text(), "1.")]/../td/div/span/b'):
                # current quest is the firs quest in the series, no series requirements
                pass
            else:
                previous_quest = selector.xpath(
                    'tr/td/div/b/../../../preceding-sibling::'
                    'tr[1]/td/div/a')
                if previous_quest:
                    self.parse_requirements(previous_quest, quest)
                else:
                    # previous quest is either horde or alliance or both
                    previous_alliance_quest = selector.xpath(
                        'tr/td/div/span/b/../../../../preceding-sibling::'
                        'tr[1]/td/div/span[@class="icon-alliance-padded"]/a')
                    previous_horde_quest = selector.xpath(
                            'tr/td/div/span/b/../../../../preceding-sibling::'
                            'tr[1]/td/div/span[@class="icon-horde"]/a')
                    self.parse_requirements(previous_alliance_quest, quest)
                    self.parse_requirements(previous_horde_quest, quest)

    @staticmethod
    def parse_requirements(selectors: List[Selector], quest: Quest) -> None:
        """
        parses selections of html a tags from quests

        adds given selection of quest links id as a requirement in the given quest boject
        :param selectors: selection of quests
        :param quest:quest object to store gathered info in
        :return:
        """
        for selector in selectors:
            quest_link = selector.xpath('@href').get()
            quest_id = int(quest_link.split("=")[-1].split("/")[0])
            if "requirements" in quest:
                quest["requirements"].update({quest_id})
            else:
                quest["requirements"] = {quest_id}

    def parse(self, response: SplashResponse):
        """
        default fallback parser

        :param response: splash rendered http response
        :return:
        """
        self.log(f"Failed to parse {response.url} with my parsers.")


if __name__ == '__main__':
    spider = ZoneSpider()
    print()
