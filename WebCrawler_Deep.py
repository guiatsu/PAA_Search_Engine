import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.spidermiddlewares.depth import DepthMiddleware
from File import *
import json
import re

data = {}

class WebCrawler(CrawlSpider):
    name="Crawler"

    rules = [
        Rule(LinkExtractor(), callback='parse_item', follow=True)
    ]

    start_urls = ["https://cic.unb.br/"]



    def parse_item(self,response):
        page = response.url.split("/")[-1]
        if page == "":
            page = response.url.split("/")[-2]

        page_elements = response.css("body :not(script):not(style)::text, img::attr(alt)").getall()
        text_lines = []
        text_lines_no_stop_word = []
        stop_words = set(get_stop_words())

        for i in page_elements:
            line = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ\s]","",i.strip())
            line = re.sub("\t"," ",line)
            line = re.sub("\s+"," ",line)
            line = line.strip()
            if(line != ""):
                text_lines.append(line.split(" "))
                text_lines_no_stop_word.append(line.split(" "))
        
        for i in range(len(text_lines_no_stop_word)):
            for j in text_lines_no_stop_word[i]:
                j = j.lower()
                if data.get(j) == None:
                    data[j] = {
                        "pages" : {
                            response.url : {
                                "title" : response.css("title::text").get(),
                                "occurrences" : 1,
                                "extracts" : [(" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if word.lower() == j])],
                            },
                        },
                    }
                else:
                    if data[j]["pages"].get(response.url) == None:
                        data[j]["pages"][response.url] = {
                            "title" : response.css("title::text").get(),
                            "occurrences": 1,
                            "extracts" : [(" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if word.lower() == j])],
                        }
                    else:
                        aux = data[j]["pages"][response.url]
                        aux["occurrences"] = aux["occurrences"] + 1
                        extracts = aux["extracts"]
                        extracts.append((" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if word.lower() == j]))
                        aux["extracts"] = extracts
                        data[j]["pages"][response.url] = aux



if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(WebCrawler)
    process.start()
    with open('Crawler.json','w') as out:
        json.dump(data,out)