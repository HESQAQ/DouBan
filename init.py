from urllib import request
from bs4 import BeautifulSoup as bs
import pymysql
conn = pymysql.connect(host='localhost', user='root', passwd="root", db='douban')
cur = conn.cursor()
# cur.execute("SELECT Host,User FROM user")


def getMovieList():
    response_1 = request.urlopen('https://movie.douban.com/cinema/nowplaying/xiamen/')
    html_data = response_1.read().decode('utf-8')
    # print(html_data)
    soup = bs(html_data, 'html.parser')
    nowPlaying_movie = soup.find_all('div', id='nowplaying')
    nowPlaying_movie_list = nowPlaying_movie[0].find_all('li', class_='list-item')

    #print(nowPlaying_movie)
    # print(nowPlaying_movie_list[0])
    print('---------------------------------------------------------------')
    print('---------------------------------------------------------------')

    nowPlaying_list = []
    for item in nowPlaying_movie_list:
        nowPlay_dict = {}
        nowPlay_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):
            nowPlay_dict['name'] = tag_img_item['alt']
            # values = []
            # values.append((str(nowPlay_dict['id']), str(nowPlay_dict['name'])))
            cur.execute('''insert into movie(id_movie, name) values('{0}','{1}')'''.\
                       format(nowPlay_dict['id'], nowPlay_dict['name']))
            conn.commit()
            # print(i)
            nowPlaying_list.append(nowPlay_dict)
    return nowPlaying_list


def getMovieComments(nowplaying_list):

    eachcommentlist = []
    # print(nowplaying_list[0]['id']
    for i in range(0,5):
        # print(i*20)
        num = i*20
        requrl = 'https://movie.douban.com/subject/'+nowplaying_list['id']+'/comments'+'?'+'start='+str(num)+'&limit=20'
        resp = request.urlopen(requrl)
        html_data = resp.read().decode('utf-8')
        # print(html_data)
        soup = bs(html_data, 'html.parser')
        comment_div_lists = soup.find_all('div', class_='comment')
        for item in comment_div_lists:
            print('--------------------------')
            # print(item.find_all('span', class_='short'))
            if item.find_all('span', class_='short')[0].string is not None:
                eachcommentlist.append(item.find_all('span', class_='short')[0].string)
                cur.execute('''insert into comment(id_movie, comment) values('{0}','{1}')'''.\
                           format(nowplaying_list['id'], pymysql.escape_string(item.find_all('span', class_='short')[0].string)))
                conn.commit()
    print(eachcommentlist)


def run():
    nowplaying_lists = getMovieList()
    for nowplaying_list in nowplaying_lists :
        getMovieComments(nowplaying_list)


if __name__ == '__main__':
    run()