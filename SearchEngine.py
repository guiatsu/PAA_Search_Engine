import json
from os import terminal_size
import re
from Parser import Parser

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

    def Process(self, search_terms):
        search_results = []

        for w in search_terms:
            if w not in ["AND", "OR", "-"]:
                #ocorrencias.append(self.data.get(w).get("pages").get(list(self.search(w))[0]))
                if w.startswith("\""):
                    search_results.append(set(self.String(w)))
                else:
                    search_results.append(set(self.search(w)))
            else:
                if w == "AND":
                    search_results.append(self.And(search_results.pop(), search_results.pop()))
                elif w == "OR":
                    search_results.append(self.Or(search_results.pop(), search_results.pop()))
                elif w == "-":
                    search_results.append(self.Not(search_results.pop(), search_results.pop()))

        print(search_results)

if __name__ == "__main__":
    SE = SearchEngine()
    P = Parser()
    ls = P.get_query_terms(P.transform_query(input("Google it: ")))
    print(ls, "\n")
    #print(SE.And(SE.search("bancos"),SE.search("de")))
    SE.Process(ls)
    #print(SE.Or(SE.search("react"), SE.search("bootstrap")))
    #print(SE.String("ir pará"))