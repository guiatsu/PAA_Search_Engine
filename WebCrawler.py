import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from File import *
import json

data = {}
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
        self.parse_page(response)
        yield from response.follow_all(links, self.parse_page)

    def parse_page(self,response):
        page = response.url.split("/")[-1]
        if page == "":
            page = response.url.split("/")[-2]

        page_elements = response.css("body :not(script)::text, img::attr(alt)").getall()
        text_lines = []
        text_lines_no_stop_word = []
        stop_words = set(get_stop_words())
        for i in page_elements:
            if(i.strip() != ""):
                text_lines.append(i.strip().split(" "))
                text_lines_no_stop_word.append([x for x in i.strip().split(" ") if x not in stop_words])
        for i in range(len(text_lines_no_stop_word)):
            for j in text_lines_no_stop_word[i]:
                if data.get(j) == None:
                    data[j] = {
                        "pages" : {
                            response.url : {
                                "ocurrences" : 1,
                                "extracts" : [(text_lines[i],[i for i,word in enumerate(text_lines[i]) if word == j])],
                            },
                        },
                    }
                else:
                    if data[j]["pages"].get(response.url) == None:
                        data[j]["pages"][response.url] = {
                            "ocurrences": 1,
                            "extracts" : [(text_lines[i],[i for i,word in enumerate(text_lines[i]) if word == j])],
                        }
                    else:
                        aux = data[j]["pages"][response.url]
                        aux["ocurrences"] = aux["ocurrences"] + 1
                        extracts = aux["extracts"]
                        extracts.append((text_lines[i],[i for i,word in enumerate(text_lines[i]) if word == j]))
                        aux["extracts"] = extracts
                        data[j]["pages"][response.url] = aux
        # filename = f'pagename-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        # aux = {
        #     "name": page,
        #     "url": response.url,
        #     "body": page_text,
        # }
        # data.append(aux)

        
process = CrawlerProcess()

process.crawl(WebCrawler)
process.start()
with open('Crawler.json','w') as out:
    json.dump(data,out)
