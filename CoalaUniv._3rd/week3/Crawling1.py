'''네이버 tv의 1위 영상의 제목을 출력하기'''

import requests
from bs4 import BeautifulSoup

raw = requests.get('https://tv.naver.com/r/', headers = {'User-Agent':'Mozilla/5.0'})

html = BeautifulSoup(raw.text,'html.parser')
#BeautifulSoup이라는 라이브러리는 String클래스의 값을 살아있는 HTML문서로 바꾸어 준다. 

clips = html.select("div.inner")

title = clips[0].select_one("dt.title")

print(title.text.strip())