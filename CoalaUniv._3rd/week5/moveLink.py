import requests
from bs4 import BeautifulSoup



raw = requests.get('https://movie.naver.com/movie/running/current.nhn', headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text, 'html.parser')
movie = html.select('dl.lst_dsc')

for m in movie:
    title = m.select_one('dt.tit a')
    print('='*50)
    print('제목:', title.text)
    
    url = title.attrs['href']
    #BS.attrs['속성이름'] : 선택한 코드에서 원하는 속성의 속성값을 저장한다.해당하는 속성이 없는 경우 에러가 발생한다. 
    
    raw_each = requests.get('https://movie.naver.com'+url, headers = {'User-Agent':'Mozilla/5.0'})
    html_each = BeautifulSoup(raw_each.text, 'html.parser')
    
    reply = html_each.select('div.score_result li')
    print('-'*50)
    print('평점과 댓글:')
    for r in reply:
        score = r.select_one('div.star_score em').text.strip()
        reply = r.select_one('div.score_reple p').text.strip()
        print(score,reply)
        