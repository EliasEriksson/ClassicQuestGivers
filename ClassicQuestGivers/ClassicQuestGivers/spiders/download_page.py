from scrapy import Spider
from scrapy.http.response import Response
import scrapy_splash


class ZoneSpider(Spider):
    name = "quests"

    def start_requests(self):
        urls = ["https://classic.wowhead.com/quest=3113/encrypted-memorandum"]

        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse)

    def parse(self, response: Response):
        page = response.url.split("/")[-2].replace("=", "-")
        filename = f"{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"saved file {filename}")

