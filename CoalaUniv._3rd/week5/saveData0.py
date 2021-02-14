import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

urlretrieve('http://movie-phinf.pstatic.net/20190417_250/1555465', 'img/어벤져스.png') #img폴더에 저장하기.
#해당하는 주소에 저장되어 있는 데이터를 파일이름으로 저장한다. 