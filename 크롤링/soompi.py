from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import googletrans

translator = googletrans.Translator()

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(chrome_options= options)
browser.maximize_window()
url = 'https://www.soompi.com/latest'
browser.get(url)
for _ in range(3):
    browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[4]/div/div[2]/a').click()
    time.sleep(1)


print('start')
soup = BeautifulSoup(browser.page_source,"lxml")
data = soup.find_all('div',attrs={'class':'thumbnail-wrapper'})
articles = []
for d in data:
    src = d.find('a')['href']
    articles.append(f'https://www.soompi.com{src}')

news=[]
for i,article in enumerate(articles[:5]):
    img_cnt = 1
    mov_cnt = 1
    tmp = {}
    res = requests.get(article)
    soup = BeautifulSoup(res.text,'lxml')
    title = soup.find('div',attrs={'class':'article-info'})
    tmp['title'] = translator.translate(title.find('h1').text,dest='ko').text
    thumb = soup.find('span',attrs={'class':'image-wrapper'})
    tmp['domain'] = 'www.soompi.com'
    tmp['link'] = article

    content = soup.find('div',attrs={'class':'article-wrapper'})
    texts = content.find_all('p')
    tmp_txt = []
    for idx,text in enumerate(texts):
        isimg = text.find('img')
        ismov = text.find('span',attrs={'class':'embed-youtube'})
        if isimg:
            imgs = text.find_all('img')
            for n,img in enumerate(imgs):
                if img.parent.name=='a':
                    continue
                tmp_txt.append(f'<img {img_cnt}> {img["data-src"]}')
                img_cnt += 1
        elif ismov:
            mov = ismov.find('iframe')
            tmp_txt.append(f'<mov {mov_cnt}> {mov["data-src"]}')
            mov_cnt += 1
        else:
            if text.text.replace(' ','') == 'WatchNow':
                tmp_txt = tmp_txt[:-2]
                break
            elif "Source (1)" in text.text:
                break
            try:
                tmp_txt.append(translator.translate(text.text,dest='ko').text)
            except:
                continue
            # tmp_txt.append(translator.translate(text.text,dest='ko').text)
    txt = '\n\n '.join(tmp_txt)
    tmp['content'] = txt
    
    news.append(tmp)
for n in news:
    print("제목:",n['title'])
    print(n['content'])