import requests
import json
from urllib import parse
import math
from music_db import insert_data
from  concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import datetime
headers={'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'no-cache',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'referer':'https://y.qq.com/portal/player.html',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400'
         }
#根据url下载歌曲
def download(songmid):
    session = requests.session()
    #params = url.rsplit('/',1)[1].split('.')[0]     #获取url中的ddler参数
    params=songmid
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid='+params+'&filename=C400'+params+'.m4a&guid=9082027038'
    response = session.get(url,headers=headers)
    response = json.loads(response.text)
    vkey = response['data']['items'][0]['vkey']

    music_url = 'http://dl.stream.qqmusic.qq.com/C400'+params+'.m4a?vkey='+vkey+'&guid=9082027038&uin=0&fromtag=66'
    response = session.get(url=music_url, stream=True,headers=headers)
    with open('music{}.mp3'.format(params), 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
#获取歌手信息
def get_singer_data(mid):
    url='https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&ct=24&singermid={}&order=listen&begin=0&num=10'.format(mid)
    html=requests.session()
    content=html.get(url,headers=headers).json()
    songs_num=content['data']['total']
    pagecount=int(math.floor(int(songs_num)/10))
    for page in range(pagecount):
        url='https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&ct=24&singermid={}&order=listen&begin=0&num={}'.format(mid,page)
        r=html.get(url,headers=headers)
        songs=r.json()['data']['list']
        datas=dict()
        for song in songs:
            print(song)
            datas['song_name']=song['musicData']['songname']
            datas['song_ablum']=song['musicData']['albumname']
            datas['song_mid']=song['musicData']['songmid']
            datas['song_singer']=song['musicData']['singer'][0]['name']
            download(datas['song_mid'])
            insert_data(datas)
            datas={}
def get_singer_mid(index):
    #index=1---27
    data='{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":%s,"sin":0,"cur_page":1}}}'%(str(index))
    url='https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI898272539416227&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(parse.quote(data))
    html=requests.get(url).json()
    total=html['singerList']['data']['total']
    pages=int(math.floor(int(total)/80))
    thread_number=pages
    Thread=ThreadPoolExecutor(max_workers=thread_number)
    for page in range(1,pages):
        data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer","method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":%s,"sin":0,"cur_page":%s}}}' % (
            str(index),str(page))
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI898272539416227&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={}'.format(
            parse.quote(data))
        html=requests.get(url,headers=headers).json()
        sings=html['singerList']['data']['singerlist']
        for sing in sings:
            #get_singer_data(sing['singer_mid'])
            Thread.submit(get_singer_data,sing['singer_mid'])

def myProcess():
    with ProcessPoolExecutor(max_workers=27) as exe:
        for i in range(1,28):
            exe.submit(get_singer_mid,i)

def main():
    myProcess()

if __name__ == '__main__':
    main()