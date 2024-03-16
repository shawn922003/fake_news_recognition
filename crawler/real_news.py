import time
import random
import requests
from bs4 import BeautifulSoup
import json


saving_file='dataset/real_article.txt'
NUMBER_OF_ARTICLE=2000

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

# udn 聯合新聞網，不同網頁版型範例
# https://udn.com/news/story/6809/4690414
# https://udn.com/news/story/6904/4698001   # https://udn.com/umedia/story/12762/4697096
# https://udn.com/news/story/6809/4699983   # https://global.udn.com/global_vision/story/8663/4698371
# https://udn.com/news/story/6809/4699958   # https://opinion.udn.com/opinion/story/120611/4698526
# https://udn.com/news/story/6812/4700330   # 跳轉"會員專屬內容"


def get_news_list(page_num=3):
    """爬取新聞列表"""
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        channelId = 1
        cate_id = 0
        type_ = 'breaknews'
        query = f"page={page+1}&channelId={channelId}&cate_id={cate_id}&type={type_}"
        news_list_url = base_url + '?' + query
        print(news_list_url)
        # https://udn.com/api/more?page=2&channelId=1&cate_id=0&type=breaknews
        
        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        news_list.extend(news_data['lists'])

        time.sleep(random.uniform(1, 2))

    return news_list

def get_news_content(link):
    url=f'https://udn.com'+link
    r=requests.get(url,headers=HEADERS)

    a=r.text

    soup = BeautifulSoup(r.content, 'html.parser')

    # 尋找所有class為'article-content__paragraph'的標籤
    
    paragraphs = soup.find_all('section', class_='article-content__editor')
    if paragraphs!=[]:
        p=paragraphs[0].get_text()
    else:
        p=""

    return p



if __name__ == "__main__":
    news_list = get_news_list(page_num=NUMBER_OF_ARTICLE//20)
    # print(news_list[0])
    print(f"共抓到 {len(news_list)} 篇新聞")
    articles=[]
    for news in news_list:
        content=get_news_content(news['titleLink'])
        if content!="":
            articles.append(content)

    with open(saving_file,'w',encoding='UTF-8') as file:
        file.write(json.dumps(articles))

    