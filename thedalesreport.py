from bs4 import BeautifulSoup
import requests
import re
import os

url = input()
res = requests.get(url)
soup = BeautifulSoup(res.text,'lxml')

data = {}
title = soup.find('span',attrs={'class':'post-title'})
data['title'] = title.text

day = soup.find('time',attrs={'class':'post-published updated'})
data['time'] = day['datetime'].replace('T',' ')[:19]

content = soup.find('div',attrs={'class':'entry-content clearfix single-post-content'})
content = map(str,(content.find_all(re.compile(r'(p|h2|h3)'))[:-1]))
content_txt = '\n'.join(content)
tmp_txt = re.sub('h[0-9]',"b",content_txt)
data['content'] = re.sub('id.*"','style="font-size:24px;"',tmp_txt)

img = soup.find('div',attrs={'class':'single-featured'}).find('img')
img_url = img['data-src']
img_res = requests.get(img_url)
image = img_res.content
path = f'./thedalesreport/{title.text.replace("?","")}'
path = path.replace(":"," ")
os.mkdir(path)

with open(f'{path}/img.jpg','wb') as f:
    f.write(image)

with open(f'{path}/text.txt','w',encoding='UTF-8') as f:
    for key,value in data.items():
        f.write(f'{key}:{value}\n')