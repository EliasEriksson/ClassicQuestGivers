from typing import List
from scrapy import Spider
from scrapy.http.response import Response
from scrapy.selector.unified import Selector
from ..items import Quest
import scrapy_splash


class ZoneSpider(Spider):
    name = "wowhead"
    base_url = "https://classic.wowhead.com"

    def start_requests(self):
        urls = ["https://classic.wowhead.com/dun-morogh#quests"]

        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse_zone)

    def parse_quick_facts(self, selector: Selector, quest: Quest):
        result = selector.re(r"Start:\s(.*</a>)")
        if result:
            element = Selector(text=result[0])
            quest["npc"] = element.xpath("//a/text()").get()
            quest["npc_link"] = self.base_url + element.xpath("//a/@href").get()
        else:
            quest["npc"] = "Unknown"
            quest["npc_link"] = "Unknown"

    def parse_quest(self, response: Response):
        quest = response.meta.get("quest")
        self.parse_quick_facts(response.xpath('//*[@id="infobox-contents-0"]/ul/li/div/span'), quest)
        yield quest

    def parse_zone(self, response: Response):
        # TODO parse for faction
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

            yield scrapy_splash.SplashRequest(url=quest["link"], callback=self.parse_quest, meta={"quest": quest})

    def parse(self, response):
        self.log("Failed to parse with my parsers.")
