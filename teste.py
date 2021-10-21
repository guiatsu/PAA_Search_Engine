import json

file = open('Crawler.json')
data = json.load(file)
for i in data:
    print(i["name"])
# print(data.items())