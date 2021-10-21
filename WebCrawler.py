import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
import json

data = []
class WebCrawler(scrapy.Spider):
    name="Crawler"
    def start_requests(self):
        # start_urls = ['http://maratona.sbc.org.br/']
        # start_urls = ['https://www.youtube.com/']
        start_urls = ['https://www.unb.br/']

        for i in start_urls:
            yield Request(i, self.parse) 

            
    
    def parse(self,response):
        links = response.css("a")
        teste = response.css("a::attr(href)").getall()
        self.dict = []
        # for i in teste:
        #     print(i)
        self.parse_page(response)
        yield from response.follow_all(links, self.parse_page)

    def parse_page(self,response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        page = response.url.split("/")[-1]
        if page == "":
            page = response.url.split("/")[-2]
        filename = f'pagename-{page}.html'
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        data.append( {
            "name": page,
            "url": response.url,
            "body": response.body.decode('utf-8'),
        })
        
process = CrawlerProcess()

process.crawl(WebCrawler)
process.start()
with open('Crawler.json','w') as out:
    json.dump(data,out)
