# 词频统计
import os
import jieba
import nltk
import time
from snownlp import SnowNLP
import wordcloud as wc


def get_stopwords():
    path = "../comments/stop_word.txt"
    lis = []
    with open(path, 'r', encoding='utf-8') as f:
        points = f.readlines()
        for p in points:
            if len(p) != 1:
                lis.append(p[:-1])
            else:
                lis.append(p[0])
    # 停用词列表去重
    res = list(set(lis))
    res = res.sort(key=lis.index)
    return res


class CommentAnalysis:

    def __init__(self):
        # 存放
        self.path_short_com = "../comments/short_comment/{}.csv"
        # 存放短评txt文件的位置，供jieba分词使用，分析完成后删除文件
        self.path_short_txt = "../comments/short_comment_txt/{}.txt"
        # 存放wordcloud生成图片的位置
        self.path_short_pic = "../comments/short_comment_pic/"

    '''
    返回id列表
    '''

    def get_id_list(self, path):
        id_list = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                film_info = line.split(',')
                film_id = film_info[-1][:-1]
                film_title = film_info[0]
                id_list.append((film_id, film_title))
        return id_list

    '''
    将存放短评的csv文件中的短评提取出来，转换为对应的txt文件，方便分词部分使用
    film_id: 电影id
    n: n=0 返回所有短评的str, n=1返回短评列表
    '''

    def com2txt(self, film_id, n):
        com_path = self.path_short_com.format(film_id)
        txt_path = self.path_short_txt.format(film_id)
        coms = ''
        coms_list = []
        # 没有txt文件就从comment源文件获取，有txt文件了就直接读
        if not os.path.exists(txt_path):
            with open(com_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    t = line.split('$')[-1]
                    coms += (t + '$')
                    coms_list.append(t)
            with open(txt_path, 'w', encoding='utf-8') as txt:
                txt.write(coms)
        else:
            with open(txt_path, 'r', encoding='utf-8') as txt:
                coms = txt.read()
                coms_list = coms.split('$')[:-1]
        return coms_list if n else coms

    '''
    读取存放短评的csv文件，返回split过后的二维数组
    '''

    def com2list(self, film_id):
        com_path = self.path_short_com.format(film_id)
        coms_list = []
        if not os.path.exists(com_path):
            with open(com_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    coms = line.split('$')
                    coms_list.append(coms)
        else:
            print("{}: file not exist".format(com_path))
        return coms_list

    '''    
    jieba分词，返回分词结果list
    '''

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

    '''    
    文本情感分析，基于snownlp库，分析影评的情感分数是否符合预期
    '''

    def text_motion(self, text):
        path = "../most_pop_film.csv"
        id_list = self.get_id_list(path)
        for f_id, f_title in id_list:
            print("电影名称： {}".format(f_title))
            f_csv = self.com2list(f_id)

        pass

    '''    
    文本情感分析，基于snownlp库，分析影评的情感分数是否极端化
    '''

    def text_motion_ex(self, f_id):
        com_list = self.com2list(f_id)
        com_num = len(com_list)
        # sw_score = []
        res = 0
        for com in com_list:
            res += SnowNLP(com).sentiments
        res = 0.8 * res / com_num
        return res
        pass

    # 主方法
    def run(self, args):
        assert len(args) != 0
        # 词频
        if args[0] == '0':
            pass
        # 情感趋向分析
        elif args[0] == '1':
            
            pass
        # 情感极性分析
        elif args[0] == '2':
            pass
        else:
            print("Invalid input of test code.")
        print("---------- Finish ----------")


if __name__ == '__main__':
    # 测试类型，0为分词和词云，1为情感分析
    test_code = input("Test Num: ")
    # 可输入具体的电影id，不指定则输入0
    test_f_id = input("Film id: ")
    ca = CommentAnalysis()
    ca.run([test_code, test_f_id])

    # f_id = '30282387'
    # ts = ca.com2txt(f_id, 0)
    # jb_lis = ca.test_jieba_list(ts, f_id)
    # col = ca.collect_count(jb_lis)
    # for i in range(20):
    #     word, count = col[i]
    #     print('{0:<15}{1:>5}'.format(word, count))
    # ca.test_wordcloud(jb_lis, f_id)
    # os.remove("comments/short_comment_txt/{}.csv".format(film_id))
