import json

FILE="fake_article.txt"

articles=[]

with open(FILE,'r',encoding='UTF=8') as file:
    articles=json.loads(file.read())


# for i in articles:
#     print(i)
#     print()
    
print(len(articles))