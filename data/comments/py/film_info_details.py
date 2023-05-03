import requests
from bs4 import BeautifulSoup
import re
import os


res_path = "../comments/film_info.csv"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Cookie": "ll=\"118282\"; bid=2FWA5hmFNE0; __gads=ID=b7838384056e8a41-221e0a9df0dc0015:T=1680440281:RT=1680440281:S=ALNI_MZ3Jn-AU5gmKvU0C1hKLIIODDaJmg; ct=y; __utmc=30149280; ap_v=0,6.0; __utma=30149280.915297433.1679663654.1681030236.1681054094.7; __utmb=30149280.0.10.1681054094; __utmz=30149280.1681054094.7.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/qq_44988175/article/details/127096889; __gpi=UID=00000bea5cf5b656:T=1680440281:RT=1681054153:S=ALNI_MafT6K0MFQTbHWnX16Y5WOqoqYjTQ; dbcl2=\"269613122:7WY2e3vQ9ac\"; ck=xi1N; frodotk_db=\"1aed5ac94973d37d50c8105bdc5b7a77\"; push_noty_num=0; push_doumail_num=0"}

id_list = []
with open('../comments.', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines[1:]:
        film_info = line.split(',')
        film_id = film_info[-1][:-1]
        film_title = film_info[0]
        id_list.append((film_id, film_title))