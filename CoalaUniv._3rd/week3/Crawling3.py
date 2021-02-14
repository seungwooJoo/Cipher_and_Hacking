'''네이버 뉴스에서 3페이지까지 뉴스 제목기사 출력하기.'''

import requests
from bs4 import BeautifulSoup



for page in range(1,22,10):
    raw = requests.get('https://search.naver.com/search.naver?where=news&query=대한민국&start='+str(page), headers = {'User-Agent':'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, 'html.parser')

    articles = html.select('div.group_news > ul li.bx')
    
    for article in articles:
        title = article.select_one('div.group_news > ul li.bx a.news_tit').text.strip()
        print((page//10)+1, 'page -',articles.index(article)+1,'.',title)

        
        