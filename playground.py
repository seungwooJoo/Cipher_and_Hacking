from urllib.request import urlopen

url = 'http://www.naver.com/mastuura/miki/love/seungwoo/joo'

tmp = url.split('/')
parent = '/'.join(tmp[2:-1])
print(parent)