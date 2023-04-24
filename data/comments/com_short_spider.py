import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import time
import random
import re
import os


# Python爬虫 爬取电影影片短评
class Spider:

    # 一些初始化
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Cookie": "ll=\"118282\"; bid=2FWA5hmFNE0; __gads=ID=b7838384056e8a41-221e0a9df0dc0015:T=1680440281:RT=1680440281:S=ALNI_MZ3Jn-AU5gmKvU0C1hKLIIODDaJmg; ct=y; __utmc=30149280; ap_v=0,6.0; __utma=30149280.915297433.1679663654.1681030236.1681054094.7; __utmb=30149280.0.10.1681054094; __utmz=30149280.1681054094.7.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/qq_44988175/article/details/127096889; __gpi=UID=00000bea5cf5b656:T=1680440281:RT=1681054153:S=ALNI_MafT6K0MFQTbHWnX16Y5WOqoqYjTQ; dbcl2=\"269613122:7WY2e3vQ9ac\"; ck=xi1N; frodotk_db=\"1aed5ac94973d37d50c8105bdc5b7a77\"; push_noty_num=0; push_doumail_num=0"
        }
        self.url = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&status=P&sort=new_score"
        self.filepath = "comments/{}/{}.csv"

    # 获取电影id和title列表,从两个整合过后的csv文件里获取
    def get_id_list(self, path):
        id_list = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                film_info = line.split(',')
                film_id = film_info[-1][:-1]
                film_title = film_info[0]
                id_list.append((film_id, film_title))
        # print(id_list)
        return id_list

    # 构造url_list
    def make_url_list(self, film_id):
        url_list = []
        for i in range(30):
            url_list.append(self.url.format(film_id, i * 20))
        return url_list

    # 检测某电影是否已经爬完整，方便脚本中断重新爬取时跳过以节省时间，0就是没爬完
    def check_output(self, path, good):
        # 已存在以id命名的csv文件
        if not os.path.exists(path):
            return 0
        # good 表示检测是否为以id命名的csv文件，若不是则重新检测文件完整性
        if good:
            return 1
        with open(path, 'r', encoding='utf-8') as f:
            lis = f.readlines()
            # print(lis[-1].split('$'))
            if lis[-1].split('$')[0] == '599':
                return 1
            else:
                return 0

    # 获取单页短评内容，交由后续解析
    def res_decode(self, url):
        res = requests.get(url=url, headers=self.headers)
        bs = BeautifulSoup(res.text, 'lxml')
        return bs

    # 将列表data添加到大列表coll中
    def data_concat(self, coll, data):
        for item in data:
            coll.append(item.replace('\n', ""))
        return coll

    # 检查某页数据长度是否对应，有问题则返回-1，舍去该页数据，无问题则返回长度
    def check_length_same(self, datalist):
        b = len(set(datalist))
        if b > 1:
            print('invalid page: ' + datalist)
            return -1
        else:
            return datalist[0]

    def run(self):
        print("-----Spider begin-----")
        path_list = ["most_pop_film", "most_score_film"]
        start_time = time.time()
        finish_task = 0
        for ts in range(2):
            id_list = self.get_id_list(path_list[ts] + '.csv')
            # 每部电影
            for film_info in id_list:
                # if film_info[0] != "1291543":
                #     continue
                finish_task += 1
                print("Begin task: %d" % finish_task)
                output_path = self.filepath.format(path_list[ts], film_info[0])
                exist_path = self.filepath.format(path_list[ts], film_info[1])
                print("Film id: %s   Film name: %s" % (film_info[0],film_info[1]))
                if self.check_output(output_path, 1):
                    continue
                if self.check_output(exist_path, 0):
                    os.rename(exist_path, output_path)
                    continue
                url_list = self.make_url_list(film_info[0])
                t = 0
                movie_id = []
                movie_title = []
                movie_comments_user = []  # 用户名
                movie_comments_time = []  # 发布时间
                movie_comments_vote = []  # 被点赞数
                movie_comments_text = []  # 评论内容

                # 每页评论
                for url in url_list:
                    page = self.res_decode(url)

                    # 被点赞数
                    vote = page.find_all(class_="votes vote-count")
                    vote = re.findall('votes vote-count">(.*?)</span>', str(vote))
                    # 用户名
                    info = page.find_all(class_='comment-info')
                    user = re.findall('href.*?/">(.*?)</a>', str(info))
                    # 发布时间
                    c_time = page.find_all(class_='comment-time')
                    c_time = re.findall('title="(.*?)"', str(c_time))
                    # 评论内容
                    text = page.find_all(class_='short')
                    text = re.findall('"short">((?:.|\n)*?)</span>', str(text))

                    # 检查四项数据长度是否对应
                    len_list = [len(vote), len(user), len(c_time), len(text)]
                    # print(len_list)
                    length = self.check_length_same(len_list)
                    if length >= 0:
                        # 单页数据添加进该部电影的数据list
                        movie_comments_vote = self.data_concat(movie_comments_vote, vote)
                        movie_comments_user = self.data_concat(movie_comments_user, user)
                        movie_comments_time = self.data_concat(movie_comments_time, c_time)
                        movie_comments_text = self.data_concat(movie_comments_text, text)
                        for i in range(length):
                            movie_id.append(film_info[0])
                            movie_title.append(film_info[1])
                        print("page %d finish" % t)
                    t += 1
                    time.sleep(random.random() * 3)

                # print([len(movie_id), len(movie_title), len(movie_comments_user), len(movie_comments_time),
                #        len(movie_comments_vote), len(movie_comments_text)])

                dataframe = pd.DataFrame({
                    "movie_id": movie_id,
                    "movie_title": movie_title,
                    "comment_user": movie_comments_user,
                    "comment_time": movie_comments_time,
                    "comment_vote": movie_comments_vote,
                    "comment_text": movie_comments_text
                })
                # 以$作为分隔符
                dataframe.to_csv(output_path, encoding='utf-8', sep='$')
                end_time = time.time()
                print("-----Spider of film %s finish at %f s-----" % (film_info[0], end_time - start_time))
                print("Finished task: %d" % finish_task)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
