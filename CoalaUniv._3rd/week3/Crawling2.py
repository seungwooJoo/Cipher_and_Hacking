'''네이버tv 인기영상 top100개의 제목 출력하기'''

import requests
from bs4 import BeautifulSoup

raw = requests.get('https://tv.naver.com/r/', headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, 'html.parser')

titles = {}
rank =1

clips = html.select('div.inner')

for clip in clips:
    title = clip.select_one('strong.tit').text.strip()
    titles[rank] = title
    rank+=1
    
clips = html.select('div.cds')
for clip in clips:
    title = clip.select_one('tooltip').text.strip()
    titles[rank] = title
    rank+=1

# 1~3위 컨테이너 : div.inner
# 4~100위 컨테이너 : div.cds

for title in titles:
    print(title ,'위 : ', titles[title])