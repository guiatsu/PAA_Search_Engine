import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
import json
import re

data = {}
class WebCrawler(scrapy.Spider):
    name="Crawler"
    def start_requests(self):
        start_urls = [
            'https://cic.unb.br/'
        ]
        
        for i in start_urls:
            yield Request(i, self.parse) 
    
    def remove_accents(self, string):
        aux_map = string.maketrans("¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ",
                                  "SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy")
        string = string.translate(aux_map)
        return string

    def parse(self,response):
        links = response.css("a")
        self.parse_page(response)
        yield from response.follow_all(links, self.parse_page)

    def parse_page(self,response):
        page = response.url.split("/")[-1]
        if page == "":
            page = response.url.split("/")[-2]

        page_elements = response.css("body :not(script):not(style)::text, img::attr(alt)").getall()
        text_lines = []
        text_lines_no_stop_word = []

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
                j = self.remove_accents(j.lower())
                if data.get(j) == None:
                    data[j] = {
                        "pages" : {
                            response.url : {
                                "title" : response.css("title::text").get(),
                                "occurrences" : 1,
                                "extracts" : [(" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if self.remove_accents(word.lower()) == j])],
                            },
                        },
                    }
                else:
                    if data[j]["pages"].get(response.url) == None:
                        data[j]["pages"][response.url] = {
                            "title" : response.css("title::text").get(),
                            "occurrences": 1,
                            "extracts" : [(" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if self.remove_accents(word.lower()) == j])],
                        }
                    else:
                        aux = data[j]["pages"][response.url]
                        aux["occurrences"] = aux["occurrences"] + 1
                        extracts = aux["extracts"]
                        extracts.append((" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if self.remove_accents(word.lower()) == j]))
                        aux["extracts"] = extracts
                        data[j]["pages"][response.url] = aux


if __name__ == "__main__":        
    process = CrawlerProcess()

    process.crawl(WebCrawler)
    process.start()

    with open('Crawler.json','w') as out:
        json.dump(data,out)
