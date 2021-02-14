'''네이버 영화에서 장르, 감독, 배우는 같은 이름의 태그 안에 저장되어 있어 선택자로 선택이 불가능 하다. '''

import requests
from bs4 import BeautifulSoup



raw = requests.get('https://movie.naver.com/movie/running/current.nhn', headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, 'html.parser')

movie = html.select('dl.lst_dsc')

for m in movie:
    title = m.select_one('dt.tit a')
    score = m.select_one('div.star_t1 span.num')
    
    #방법1. 리스트 활용하기
    # info = m.select('dl.info_txt1 dd')
    # genre = info[0].select('a')
    # directors = info[1].select('a')
    # actors = info[2].select('a')
    
    #방법2.
    genre = m.select('dl.info_txt1 dd:nth-of-type(1) a ')    #리스트와 달리 첫번째 데이터의 인덱스가 1이다
    directors =m.select('dl.info_txt1 dd:nth-of-type(2) a ')
    actors =m.select('dl.info_txt1 dd:nth-of-type(3) a ')
    
    print('='*50)
    print('제목:', title.text)
    
    print('-'*50)
    print('평점:', score.text)
    
    print('-'*50)
    print('장르:')
    for g in genre:
        print(g.text)
        
    print('-'*50)
    print('감독:')
    for d in directors:
        print(d.text)
