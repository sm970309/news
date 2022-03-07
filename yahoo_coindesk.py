from bs4 import BeautifulSoup
import requests
import re
import os

url = input()
res = requests.get(url)
soup = BeautifulSoup(res.text,'lxml')

data = {}
tmp_title = soup.find('header',attrs={'class':'caas-title-wrapper'})
title = tmp_title.find('h1').text
# print(title)
data['title'] = title

tmp_day = soup.find('div',attrs={'class':'caas-attr-time-style'})
day = tmp_day.find('time')

data['time'] = day['datetime'].replace('T',' ')[:19]

content = soup.find('div',attrs={'class':'caas-body'})
content = map(str,content.find_all(re.compile(r'(p|h2|h3)')))
content_txt = '\n'.join(content)
tmp_txt = re.sub('h[0-9]',"b",content_txt)
data['content'] = tmp_txt

images = []
imgs = soup.find_all('div',attrs={'class':'caas-img-container'})
for idx,img in enumerate(imgs):
    img_src = img.find('img')
    img_url = img_src['data-src']
    img_res = requests.get(img_url)
    images.append(img_res.content)

path = f'./yahoo/{title.replace("?","")}'
path = path.replace(":"," ")
os.mkdir(path)

for idx,image in enumerate(images):
    with open(f'{path}/img{idx+1}.jpg','wb') as f:
        f.write(image)

with open(f'{path}/text.txt','w',encoding='UTF-8') as f:
    for key,value in data.items():
        f.write(f'{key}:{value}\n')