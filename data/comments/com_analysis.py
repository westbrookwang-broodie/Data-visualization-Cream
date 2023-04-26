import os
import jieba
import time
from nltk.corpus import stopwords

import wordcloud as wc


def get_stopwords():
    path = "comments/stop_word.txt"
    lis = []
    with open(path, 'r', encoding='utf-8') as f:
        points = f.readlines()
        for p in points:
            if len(p) != 1:
                lis.append(p[:-1])
            else:
                lis.append(p[0])
    return lis


class CommentAnalysis:

    def __init__(self):
        self.path_short_com = "comments/short_comment/{}.csv"
        # 存放短评txt文件的位置，供jieba分词使用，分析完成后删除文件
        self.path_short_txt = "comments/short_comment_txt/{}.txt"
        # 存放wordcloud生成图片的位置
        self.path_short_pic = "comments/short_comment_pic/"
        self.stopword_list = stopwords.words('chinese')

    # 将存放短评的csv文件中的短评提取出来，转换为对应的txt文件，方便后续使用,同时返回所有短评的str
    def com2txt(self, film_id):
        com_path = self.path_short_com.format(film_id)
        txt_path = self.path_short_txt.format(film_id)
        # 没有txt文件就从comment源文件获取，有txt文件了就直接读
        if not os.path.exists(txt_path):
            coms = ''
            coms_list = []
            with open(com_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    t = line.split('$')[-1]
                    coms += t
                    coms_list.append(t)
            with open(txt_path, 'w', encoding='utf-8') as txt:
                txt.write(coms)
        else:
            with open(txt_path, 'r', encoding='utf-8') as txt:
                coms = txt.read()
        return coms

    # jieba分词，返回分词结果list
    def test_jieba_list(self, txt, film_id):
        words = jieba.cut(txt)
        res = []
        # 去停用词
        swords = get_stopwords()
        for word in words:
            if word not in swords:
                res.append(word)
        return res

    # 统计词频
    def collect_count(self, jb_txt):
        res = []
        for word in set(jb_txt):
            num = jb_txt.count(word)
            res.append([word, num])
            res.sort(key=lambda x: x[1], reverse=True)
        return res

    # wordcloud生成词云
    def test_wordcloud(self, jb_txt, film_id):
        jb = " ".join(jb_txt)
        w = wc.WordCloud(
            width=1920, height=1080,
            background_color='white',
            max_words=150,
            font_path='msyh.ttc')
        w.generate(jb)
        path = self.path_short_pic + "{}.png"
        w.to_file(path.format(film_id))


if __name__ == '__main__':
    ca = CommentAnalysis()
    f_id = '30282387'
    ts = ca.com2txt(f_id)
    jb_lis = ca.test_jieba_list(ts, f_id)
    # col = ca.collect_count(jb_lis)
    # for i in range(20):
    #     word, count = col[i]
    #     print('{0:<15}{1:>5}'.format(word, count))
    ca.test_wordcloud(jb_lis, f_id)
    # os.remove("comments/short_comment_txt/{}.csv".format(film_id))

    print("Finish")
