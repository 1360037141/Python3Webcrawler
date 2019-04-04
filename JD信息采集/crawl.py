import requests
from bs4 import BeautifulSoup
import csv

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Referer': 'https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page=9'
}

def get_html(keyword,pages):
    n=1
    for i in range(pages):
        store = []
        url="https://search.jd.com/Search?keyword={}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={}"\
            .format(keyword,n)
        n+=2
        html=requests.get(url,headers=headers)
        html.encoding='utf8'
        soup=BeautifulSoup(html.text,'lxml')
        books=soup.findAll('li',attrs={'class':'gl-item'})

        for book in books:
            data = {}
            name=book.find('div',attrs={'class':'p-name p-name-type-2'}).find("a").find('em').get_text()
            print(name)
            price=book.find('div',attrs={'class':'p-price'}).find('strong').find('i').get_text()
            try:
                shop=book.find('div',attrs={'class':'p-shop'}).find("span").find('a').get_text()
            except:
                shop='暂无出版社'
            try:
                commit=book.find('div',attrs={'class':'p-commit'}).find('strong').find('a').get_text()
            except:
                commit='无人评价'
            data['name']=name
            data['price']=price
            data['shop']=shop
            data['commit']=commit
            store.append(data)
        sort_data(store,keyword)
        store=[]
auto_distance=[]#去重

def sort_data(data,name):
    with open(name+'.csv','a',newline='',encoding='utf8')as f:
        writer=csv.writer(f)
        for i in data:
            if i['name'] not in auto_distance:
                writer.writerow((i['name'],i['price'],i['shop'],i['commit']))
                auto_distance.append(i['name'])