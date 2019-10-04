from typing import List
from pathlib import Path
from scrapy import Spider
from scrapy.selector.unified import Selector
from scrapy_splash import SplashResponse
from ..items import Quest
import scrapy_splash
from .. import PROJECT_ROOT


class ZoneSpider(Spider):
    name = "wowhead"
    base_url = "https://classic.wowhead.com"

    def build_urls(self) -> List[str]:
        """
        builds the start urls based on the names in zones.txt in the project root

        :return: urls
        """
        path = Path(PROJECT_ROOT).joinpath("zones.txt")
        with open(str(path)) as zones:
            urls = [f"{self.base_url}/{zone.lower().strip().replace(' ', '-')}#quests"
                    for zone in zones]
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
            quest["id"] = int(quest["link"].split("=")[-1])
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
        self.parse_quick_facts(response.xpath('//*[@id="infobox-contents-0"]/ul/li/div/span'), quest)
        yield quest

    def parse_quick_facts(self, selector: Selector, quest: Quest):
        """
        parses the quick facts section on a wowhead quest page

        :param selector: selector of the quick facts section
        :param quest: quest item to store gathered info in
        :return:
        """
        result = selector.re(r"Start:\s(.*</a>)")
        if result:
            element = Selector(text=result[0])
            quest["npc"] = element.xpath("//a/text()").get()
            quest["npc_link"] = self.base_url + element.xpath("//a/@href").get()
        else:
            quest["npc"] = "Unknown"
            quest["npc_link"] = "Unknown"

    def parse(self, response: SplashResponse):
        """
        default fallback parser

        :param response: splash rendered http response
        :return:
        """
        self.log(f"Failed to parse {response.url} with my parsers.")
