import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



raw = requests.get('https://movie.naver.com/movie/running/current.nhn', headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, 'html.parser')
movie = html.select('dl.lst_dsc')

for m in movie:
    title = m.select_one('dt.tit a')
    print('='*50)
    print('제목:', title.text)
    
    url = title.attrs['href']
   
    
    raw_each = requests.get('https://movie.naver.com'+url, headers = {'User-Agent':'Mozilla/5.0'})
    html_each = BeautifulSoup(raw_each.text, 'html.parser')
    
    img = html_each.select_one('div.mv_info_area div.poster img')
    src = img.attrs['src']        #attrs기능을 사용해서 src값을 저장한다.
    
    urlretrieve(src, '/'+title.text[:4]+'.png')
    print('-'*40)
    print(title, '포스터 저장 완료!')