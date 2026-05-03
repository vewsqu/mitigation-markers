import scrapy
from scrapy.crawler import CrawlerProcess
import nest_asyncio
import re

nest_asyncio.apply()


class RBCSpider(scrapy.Spider):
    name = "rbc"

    custom_settings = {
        'LOG_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0',
        }
    }

    def start_requests(self):
        url = ""  
        yield scrapy.Request(url, callback=self.parse_rss)

    def parse_rss(self, response):
        links = response.css('item link::text').getall()

 
        links = links[:10]

        for i, link in enumerate(links, 1):
            yield response.follow(
                link,
                callback=self.parse_article,
                meta={'index': i}
            )

    def clean_text(self, text_list):
    
        text = " ".join(text_list)

   
        text = re.sub(r'\s+', ' ', text).strip()

       
        sentences = re.split(r'(?<=[.!?]) +', text)

        
        grouped = []
        for i in range(0, len(sentences), 3):
            chunk = " ".join(sentences[i:i+3])
            grouped.append(chunk)

        return "\n\n".join(grouped)

    def parse_article(self, response):
        index = response.meta['index']

        title = response.css('h1::text').get()
        title = title.strip() if title else "Без названия"

        text_list = response.css(
            'div[itemprop="articleBody"] p::text'
        ).getall()


        if not text_list:
            text_list = response.css('p::text').getall()

        text = self.clean_text(text_list)

        print("=" * 90)
        print(f"ARTICLE: {index}\n")
        print("TITLE:")
        print(title, "\n")
        print("URL:")
        print(response.url, "\n")
        print("TEXT:")
        print(text, "\n")


process = CrawlerProcess()
process.crawl(RBCSpider)
process.start()
