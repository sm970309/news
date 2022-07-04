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
for i,link in enumerate(links):
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
    for child in content.children:
        
        if "추천" in child.text:
            break
        tmp_txt.append(str(child).replace("\xa0", " "))
    tmp['content'] = ''.join(tmp_txt[1:])
    
    data.append(tmp)

post_url = 'https://muggles.co.kr/admin/api_news_insert.php'
for d in data:
    response = requests.post(post_url,data=d)
    print(response.json()['error'])