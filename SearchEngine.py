import json
from os import terminal_size
import re
from Parser import Parser

class SearchEngine:
    def __init__(self):
        file = open("Crawler.json","r")
        self.data = json.load(file)
        self.titles = {}
    
    def search(self,word):
        word = word.lower()
        sites = self.data.get(word)
        pages = {}.keys()
        extracts = {}
        if sites != None:
            pages = sites["pages"].keys()
            for i in pages:
                self.title[i] = sites["pages"][i]["title"]
                if(extracts.get(i) == None):
                    extracts[i] = []
                for j in sites["pages"][i]["extracts"]:
                    extracts[i].append(j[0])

        return pages,extracts,set([word])

    def And(self,word1,word2):

        urls = word1[0] & word2[0]
        words = word1[2].union(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = set(extracts1[i])
            page2 = set(extracts2[i])
            extracts[i] = list(page1.intersection(page2))

        return urls,extracts,words

    def Or(self,word1,word2):

        urls = word1[0] | word2[0]
        words = word1[2].union(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = set(extracts1[i])
            page2 = set(extracts2[i])
            extracts[i] = list(page1.union(page2))
            

        return urls,extracts,words


    def Not(self,word1,word2):
        urls = word1[0] - word2[0]
        words = word1[2].difference(word2[2])
        extracts1 = word1[1]
        extracts2 = word2[1]
        extracts = {}
        for i in urls:
            page1 = set(extracts1[i])
            page2 = set(extracts2[i])
            extracts[i] = list(page1.difference(page2))
            print(i)
            print(page1)
            print(page2)
            print(extracts[i])

        return urls,extracts,words

    def String(self,string):
        words = string.split(" ")
        search = 0
        urls = set()
        extracts_to_return = {}
        if len(words) == 1:
            return self.search(words[0])
        else:
            search = self.search(words[0])
            for i in range(1,len(words)):
                search = self.And(search,self.search(words[i]))
            if search == set():
                return set(),{},set([string])
            else:
                pages = self.data.get(words[0])
                if(pages == None):
                    return set(),{},set([string])
                else:
                    pages = pages["pages"]
                    for i in search[0]:
                        self.title[i] = self.data.get(words[0])["pages"][i]["title"]
                        if(extracts_to_return.get(i) == None):
                            extracts_to_return[i] = []
                        found = False
                        extracts = pages[i]["extracts"]
                        for j in extracts:
                            aux = j[0]
                            aux = re.sub("[^A-Za-z0-9-ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ ]","",aux)
                            aux_map = aux.maketrans('¿¿¿¿¿ÁÇÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕËÜÏÖÑÝåáçéíóúàèìòùâêîôûãõëüïöñýÿ',
                                                    'SZszYACEIOUAEIOUAEIOUAOEUIONYaaceiouaeiouaeiouaoeuionyy')
                            aux = aux.translate(aux_map)
                            aux = re.sub("\t"," ",aux)
                            aux = re.sub("\s+"," ",aux)
                            aux = aux.strip()
                            if(aux.lower().find(string) == -1):
                                continue
                            else:
                                if(not found):
                                    urls.add(i)
                                extracts_to_return[i].append(j[0])
                                found = True
                        if found == False:
                            extracts_to_return.pop(i)
                    return urls,extracts_to_return,set([string])


    def get_occurences(self,elem):
        return elem[1]["occurrences"]

    def Process(self, search_terms):
        search_results = []

        for w in search_terms:
            if w not in ["AND", "OR", "-"]:
                #ocorrencias.append(self.data.get(w).get("pages").get(list(self.search(w))[0]))

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
    # P = Parser()
    # ls = P.get_query_terms(P.transform_query(input("Google it: ")))
    # print(ls, "\n")
    #print(SE.And(SE.search("bancos"),SE.search("de")))
    # SE.Process(ls)
    #print(SE.Or(SE.search("react"), SE.search("bootstrap")))
    #print(SE.String("ir pará"))
    print(SE.And(SE.search("lucero"),SE.search("jorge")), end="\n\n")
    print(SE.Or(SE.search("lucero"),SE.search("jorge")), end="\n\n")
    print(SE.Not(SE.search("lucero"),SE.search("jorge")), end="\n\n")
    print(SE.String("jorge lucero"), end="\n\n")
    print(SE.String("lucero jorge"), end="\n\n")

