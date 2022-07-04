from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

url = 'https://www.instiz.net/pt/7174765'
res = requests.get(url)
soup = BeautifulSoup(res.text,'lxml')

data = {}

data['title'] = soup.find('span',attrs={'id':'nowsubject'}).text
data['domain'] = 'www.instiz.net'

content = soup.find('div',attrs={'class':'memo_content'})
tmp_txt = []
for child in content.children:
    
    if "추천" in child.text:
        break
    
    tmp_txt.append(child)
data['content'] = str(tmp_txt[1])
data['no']=7174765



post_url = 'https://muggles.co.kr/admin/api_news_insert.php'
response = requests.post(post_url,data=data)
print(response.json())
