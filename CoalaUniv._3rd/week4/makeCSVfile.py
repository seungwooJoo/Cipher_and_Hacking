'''네이버tv 인기영상의 제목 , 채널명, 재생수, 좋아요 수를 csv 파일로 저장하기'''

import requests
from bs4 import BeautifulSoup

f= open('navertv.csv', 'w')
f.write('제목, 채널명, 재생 수, 좋아요 수\n')

raw = requests.get('https://tv.naver.com/r/', headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, 'html.parser')


clips = html.select('.cds_info')

for clip in clips:
    title = clip.select_one('dt.title').text.strip()
    chn = clip.select_one('.chn').text.strip()
    hit = clip.select_one('.hit').text.strip()
    like = clip.select_one('.like').text.strip()
    
    title = title.replace(',',' ')
    chn = chn.replace(',',' ')
    
    hit = hit.replace(',','')
    hit = hit[4:]
    
    like = like.replace(',','')
    like = like[5:]
    
    f.write(title+','+chn+','+hit+','+like+'\n')
f.close()