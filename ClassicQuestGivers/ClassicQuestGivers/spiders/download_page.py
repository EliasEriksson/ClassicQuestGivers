from scrapy import Spider
from scrapy_splash import SplashResponse
import scrapy_splash


class ZoneSpider(Spider):
    """
    Unused class but can be used to downlaod pages and save them locally by
    modefying the urls variable
    """
    name = "quests"

    def start_requests(self):
        urls = ["https://classic.wowhead.com/quest=1640/beat-bartleby"]

        for url in urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse)

    def parse(self, response: SplashResponse):
        page = response.url.split("/")[-2].replace("=", "-")
        filename = f"{page}.html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"saved file {filename}")

