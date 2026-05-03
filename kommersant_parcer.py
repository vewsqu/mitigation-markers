import scrapy
import re
from scrapy.crawler import CrawlerProcess
import nest_asyncio

nest_asyncio.apply()


class KommersantSpider(scrapy.Spider):
    name = "kommersant"

    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    def start_requests(self):
        url = ""
        yield scrapy.Request(url, headers=self.custom_headers)

    def parse(self, response):
        links = response.css('a.uho__link::attr(href)').getall()

        links = list(set(links))[:5]

        for link in links:
            yield response.follow(
                link,
                callback=self.parse_article,
                headers=self.custom_headers
            )

    def parse_article(self, response):
        title = response.css('h1::text').get()

        paragraphs = response.css(
            'div.article_text_wrapper p::text'
        ).getall()

   
        text = " ".join(p.strip() for p in paragraphs if p.strip())
        sentences = re.split(r'(?<=[.!?])\s+', text)

 
        grouped = []
        for i in range(0, len(sentences), 3):
            grouped.append(" ".join(sentences[i:i+3]))

        final_text = "\n".join(grouped)

        print("=" * 90)
        print("ARTICLE:\n")
        print("TITLE:\n", title)
        print("\nURL:\n", response.url)
        print("\nTEXT:\n", final_text)


process = CrawlerProcess()
process.crawl(KommersantSpider)
process.start()
