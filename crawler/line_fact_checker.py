
import requests
import json

NUMBER_OF_ARTICLE=3000
saving_file='dataset/fake_article.txt'

all_articles=[]
for counter in range(NUMBER_OF_ARTICLE//12):  
    # 目標URL
    url = f'https://api-fact-checker.line-apps.com/pub/v1/zhtw/articles/verified?size=12&sort=updatedAt,desc&page={counter}&'

    # 發送GET請求
    response = requests.get(url)

    # 顯示請求的狀態碼
    print(response.status_code)

    # 顯示請求回應的內容
    all_articles+=(json.loads(response.text)['content'])

fake_articles=[]
for article in all_articles:
    content=article['content']
    tag=article['tag']['zhtw']


    if tag=="不實":
        fake_articles.append(content)


with open(saving_file,'w',encoding='UTF-8') as file:
        file.write(json.dumps(fake_articles))
