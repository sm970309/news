from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re

links = []
for page in range(5):
    src = f"https://www.instiz.net/pt?page={page}&srd=1"
    res = requests.get(src)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,"lxml")
    tds = soup.find_all('td',attrs={'class':re.compile('sbj')})
    for td in tds:
        tmp = td.find('a')['href'].replace('.','').split('?')[0]
        links.append("https://www.instiz.net"+tmp)

data=[]
for i,link in enumerate(links[:2]):
    tmp = {}
    tmp_txt = []
    res = requests.get(link)
    res.raise_for_status()
    soup = BeautifulSoup(res.text,'lxml')
     
    # 제목,링크
    title= soup.find('span',attrs={'id':'nowsubject'})
    if title.find('i',attrs={'class':'fab fa-twitter'}):
        print('동영상')
        continue
    if title.find('i',attrs={'class':'fab fa-youtube'}):
        print('트위터')
        continue
    tmp['title'] = title.text
    tmp['domain'] = 'www.instiz.net'
    tmp['no'] = link.split('/')[-1]
    
    content = soup.find('div',attrs={'class':'memo_content'})
    img_cnt = 1

    for child in content.children:

        isimg = child.find('img')
        if child.name=='img':
            tmp_txt.append(f"<img {img_cnt}> {child['src']}")
            img_cnt+=1
        elif isimg and isimg!=-1:
            for img in child.find_all('img'):
                tmp_txt.append(f"<img {img_cnt}> {img['src']}")
                img_cnt+=1
        else:
            if "추천" in child.text:
                img_cnt=1
                break
        tmp_txt.append(child.text)
    print('\n'.join(tmp_txt))
    tmp['content'] = tmp_txt
    data.append(tmp)
