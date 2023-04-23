import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
import time
import random
import re


# Python爬虫 爬取电影《你的名字》影片短评
class Spider:

    # 一些初始化
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Cookie": "ll=\"118282\"; bid=2FWA5hmFNE0; __gads=ID=b7838384056e8a41-221e0a9df0dc0015:T=1680440281:RT=1680440281:S=ALNI_MZ3Jn-AU5gmKvU0C1hKLIIODDaJmg; ct=y; __utmc=30149280; ap_v=0,6.0; __utma=30149280.915297433.1679663654.1681030236.1681054094.7; __utmb=30149280.0.10.1681054094; __utmz=30149280.1681054094.7.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/qq_44988175/article/details/127096889; __gpi=UID=00000bea5cf5b656:T=1680440281:RT=1681054153:S=ALNI_MafT6K0MFQTbHWnX16Y5WOqoqYjTQ; dbcl2=\"269613122:7WY2e3vQ9ac\"; ck=xi1N; frodotk_db=\"1aed5ac94973d37d50c8105bdc5b7a77\"; push_noty_num=0; push_doumail_num=0"
        }
        self.url = "https://movie.douban.com/subject/26683290/comments?start={}&limit=20&status=P&sort=new_score"
        self.filepath = "../data/test/test.csv"

    # 构造url_list
    def make_url_list(self):
        url_list = []
        for i in range(30):
            url_list.append(self.url.format(i * 20))
        return url_list

    # 获取单页短评内容，交由后续解析
    def res_decode(self, url):
        res = requests.get(url=url, headers=self.headers)
        bs = BeautifulSoup(res.text, 'lxml')
        return bs

    # 消除空格
    def data_concat(self, coll, data):
        for item in data:
            coll.append(item)
        return coll

    def run(self):
        print("-----Spider begin-----")
        start_time = time.time()
        url_list = self.make_url_list()
        t = 0

        movie_id = []
        movie_title = []
        movie_comments_user = []  # 用户名
        movie_comments_time = []  # 发布时间
        movie_comments_vote = []  # 被点赞数
        movie_comments_text = []  # 评论内容

        for url in url_list:
            page = self.res_decode(url)

            for i in range(20):
                movie_id.append("26683290")
                movie_title.append("你的名字。")

            # 被点赞数
            vote = page.find_all(class_="votes vote-count")
            vote = re.findall('votes vote-count">(.*?)</span>', str(vote))
            movie_comments_vote = self.data_concat(movie_comments_vote, vote)

            info = page.find_all(class_='comment-info')
            # 用户名
            user = re.findall('href.*?/">(.*?)</a>', str(info))
            movie_comments_user = self.data_concat(movie_comments_user, user)

            # 发布时间
            c_time = page.find_all(class_='comment-time')
            c_time = re.findall('title="(.*?)"', str(c_time))
            movie_comments_time = self.data_concat(movie_comments_time, c_time)

            # 评论内容
            text = page.find_all(class_='short')
            text = re.findall('"short">((?:.|\n)*?)</span>', str(text))
            movie_comments_text = self.data_concat(movie_comments_text, text)

            print("page %d finish" % t)
            t += 1
            time.sleep(random.random() * 5)

            print("id: %d" % len(movie_id))
            print("title: %d" % len(movie_title))
            print("c user: %d" % len(movie_comments_user))
            print("c time: %d" % len(movie_comments_time))
            print("c vote: %d" % len(movie_comments_vote))
            print("c text: %d" % len(movie_comments_text))

        dataframe = pd.DataFrame({
            "movie_id": movie_id,
            "movie_title": movie_title,
            "comment_user": movie_comments_user,
            "comment_time": movie_comments_time,
            "comment_vote": movie_comments_vote,
            "comment_text": movie_comments_text
        })
        dataframe.to_csv(self.filepath, encoding='utf-8', sep='$')
        end_time = time.time()
        print("-----Spider finish in %f s-----" % (end_time - start_time))
        pass


if __name__ == '__main__':
    spider = Spider()
    spider.run()
