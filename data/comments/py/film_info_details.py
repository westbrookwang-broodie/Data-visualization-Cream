import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import time
import random

'''
    几个测试用例的film_id:
    30282387 银河补习班
    1424552 大决战之辽沈战役
    11510624 全民目击
'''

res_path = "../comments/film_info.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Cookie": "ll=\"118282\"; bid=2FWA5hmFNE0; __gads=ID=b7838384056e8a41-221e0a9df0dc0015:T=1680440281:RT=1680440281:S=ALNI_MZ3Jn-AU5gmKvU0C1hKLIIODDaJmg; ct=y; __utmc=30149280; ap_v=0,6.0; __utma=30149280.915297433.1679663654.1681030236.1681054094.7; __utmb=30149280.0.10.1681054094; __utmz=30149280.1681054094.7.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/qq_44988175/article/details/127096889; __gpi=UID=00000bea5cf5b656:T=1680440281:RT=1681054153:S=ALNI_MafT6K0MFQTbHWnX16Y5WOqoqYjTQ; dbcl2=\"269613122:7WY2e3vQ9ac\"; ck=xi1N; frodotk_db=\"1aed5ac94973d37d50c8105bdc5b7a77\"; push_noty_num=0; push_doumail_num=0"}
film_url = "https://movie.douban.com/subject/{}/?from=showing"
com_url = "https://movie.douban.com/subject/{}/comments?status=P"

# 获取电影id列表
id_list = []
folder_path = "../comments/short_comment"
f_lists = os.listdir(folder_path)
for path in f_lists:
    path = path.split('.')[0]
    id_list.append(path)
print(id_list)
# 获取电影详细信息

id_m = []  # 电影id
name_m = []  # 电影名
vote_m = []  # 电影总评分
peo_m = []  # 总评分人数
com_m = []  # 短评总数
star_5 = []  # 5星评分比例
star_4 = []  # 4星评分比例
star_3 = []  # 3星评分比例
star_2 = []  # 2星评分比例
star_1 = []  # 1星评分比例

i = 0
for f_id in id_list:
    # if f_id != "1422020":
    #     continue
    print("{} 电影id: {}".format(i, f_id))
    i += 1
    url = film_url.format(f_id)
    res = requests.get(url=url, headers=headers)
    page = BeautifulSoup(res.text, 'lxml')
    # 电影名
    f_name = page.find_all(property="v:itemreviewed")
    f_name = re.findall('v:itemreviewed">(.*?)</span>', str(f_name))[0]
    # print(f_name)
    # 总评分
    f_votes = page.find_all(property="v:average")
    f_votes = re.findall('property="v:average">(.*?)</strong>', str(f_votes))[0]
    # print(f_votes)
    # 总评分人数
    f_people = page.find_all(property="v:votes")
    f_people = re.findall('v:votes">(.*?)</span>', str(f_people))[0]
    # print(f_people)
    # 评分
    f_stars = page.find_all(class_="rating_per")
    f_stars = re.findall('rating_per">(.*?)</', str(f_stars))
    # print(f_stars)
    # 短评总条数
    with open('../comments/short_comment/{}.csv'.format(f_id), 'r', encoding='utf-8') as file:
        lens = len(file.readlines())-1
    if lens < 300:
        sho_len = lens
    else:
        com_len = page.find_all(href=com_url.format(f_id))
        com_len = re.findall('status=P">(.*?)</a', str(com_len))
        sho_len = "".join(filter(str.isdigit, com_len[0]))
    # print(sho_len)


    id_m.append(f_id)
    name_m.append(f_name)
    vote_m.append(f_votes)
    peo_m.append(f_people)
    com_m.append(sho_len)
    star_5.append(f_stars[0])
    star_4.append(f_stars[1])
    star_3.append(f_stars[2])
    star_2.append(f_stars[3])
    star_1.append(f_stars[4])
    time.sleep(random.random() * 3)

df = pd.DataFrame({
    "movie_id": id_m,
    "movie_name": name_m,
    "movie_vote": vote_m,
    "movie_voter": peo_m,
    "movie_5star": star_5,
    "movie_4star": star_4,
    "movie_3star": star_3,
    "movie_2star": star_2,
    "movie_1star": star_1,
    "movie_shortcom_num": com_m
})
df.to_csv(res_path, encoding='utf-8')
print("finish")
