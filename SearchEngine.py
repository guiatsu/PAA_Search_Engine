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

    def Process(self, term_list):
        found_list = []

        for i in range(len(term_list)):
            if term_list[i] not in ["AND", "OR", "-"]:
                found_list.append(set(self.search(term_list[i])))
            else:
                if term_list[i] == "AND":
                    found_list.append(self.And(found_list.pop(), found_list.pop()))
                elif term_list[i] == "OR":
                    found_list.append(self.Or(found_list.pop(), found_list.pop()))
                elif term_list[i] == "-":
                    found_list.append(self.Not(found_list.pop(), found_list.pop()))

        print(found_list)

if __name__ == "__main__":
    SE = SearchEngine()
    P = Parser()
    ls = P.get_query_terms(P.transform_query(input("Google it: ")))
    print(ls, "\n")
    #print(SE.And(SE.search("bancos"),SE.search("de")))
    SE.Process(ls)
    #print(SE.Or(SE.search("react"), SE.search("bootstrap")))
    #print(SE.String("ir pará"))