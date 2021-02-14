'''네이버tv 엑셀파일에 저장하기'''

import requests
from bs4 import BeautifulSoup
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['제목','채널','재생 수','좋아요 수'])

raw = requests.get('https://tv.naver.com/r',headers = {'User-Agent':'Mozilla/5.0'})
html = BeautifulSoup(raw.text,'html.parser')

clips  = html.select('.cds_info')

for clip in clips:
    title = clip.select_one('dt.title').text.strip()
    chn = clip.select_one('.chn').text.strip()
    hit = clip.select_one('.hit').text.strip()
    
    sheet.append([title,int(chn), int(hit), int(like)])

wb.save('naver.xlsx')