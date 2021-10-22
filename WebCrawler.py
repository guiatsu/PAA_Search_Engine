import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from File import *
import json
import re

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
            line = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ ]","",i.strip())
            line = re.sub("\t"," ",line)
            line = re.sub("\s{2,}","",line)
            line = line.strip()
            if(line != ""):
                aux_map = line.maketrans('¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ',
                                         'SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy')
                text_lines.append(line.split(" "))
                # text_lines_no_stop_word.append([x for x in line.split(" ") if x.lower().translate(aux_map) not in stop_words and len(x) > 1])
                # text_lines_no_stop_word.append([x for x in line.split(" ") if x.lower().translate(aux_map) not in stop_words and len(x) > 1])
                text_lines_no_stop_word.append(line.split(" "))
        
        for i in range(len(text_lines_no_stop_word)):
            for j in text_lines_no_stop_word[i]:
                j = j.lower()
                if data.get(j) == None:
                    data[j] = {
                        "pages" : {
                            response.url : {
                                "occurrences" : 1,
                                "extracts" : [(" ".join(text_lines[i]),[i for i,word in enumerate(text_lines[i]) if word.lower() == j])],
                            },
                        },
                    }
                else:
                    if data[j]["pages"].get(response.url) == None:
                        data[j]["pages"][response.url] = {
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
        # filename = f'pagename-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        
process = CrawlerProcess()

process.crawl(WebCrawler)
process.start()
with open('Crawler.json','w') as out:
    json.dump(data,out)
