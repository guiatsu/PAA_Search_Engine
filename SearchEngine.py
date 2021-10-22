import json
import re
class SearchEngine:
    def __init__(self):
        file = open("Crawler.json","r")
        self.data = json.load(file)
    
    def search(self,word):
        word = word.lower()
        sites = self.data.get(word)
        if sites != None:
            sites = sites["pages"].keys()
        else:
            sites = {}.keys()
        return sites

    def And(self,word1,word2):
        return word1 & word2

    def Or(self,word1,word2):
        return word1 | word2

    def Not(self,word1,word2):
        return word1-word2

    def String(self,string):
        string = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ ]","",string)
        aux_map = string.maketrans('¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ',
                                   'SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy')
        string = string.translate(aux_map)
        string = re.sub("\t"," ",string)
        string = re.sub("\s{2,}","",string)
        string = string.strip()
        words = string.split(" ")
        search = 0
        urls = set()
        if len(words) == 1:
            return self.search(words[0])
        else:
            search = self.search(words[0])
            for i in range(1,len(words)):
                search = self.And(search,self.search(words[i]))
            if search == set():
                return set()
            else:
                pages = self.data.get(words[0])
                if(pages == None):
                    return set()
                else:
                    pages = pages["pages"]
                    for i in search:
                        found = False
                        extracts = pages[i]["extracts"]
                        for j in extracts:
                            aux = j[0]
                            aux = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ ]","",aux)
                            aux_map = aux.maketrans('¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ',
                                                    'SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy')
                            aux = aux.translate(aux_map)
                            aux = re.sub("\t"," ",aux)
                            aux = re.sub("\s{2,}","",aux)
                            aux = aux.strip()
                            if(aux.lower().find(string) == -1):
                                continue
                            else:
                                found = True
                                urls.add(i)
                                break
                    return urls


    def get_occurences(self,elem):
        return elem[1]["occurrences"]


SE = SearchEngine()
print(SE.String("ir pará"))