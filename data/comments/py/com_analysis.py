# 词频统计
import os
import jieba
import time
from snownlp import SnowNLP
import wordcloud as wc
import pandas as pd
import numpy as np


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
        # 存放电影名单及相关信息文件的位置
        # 数据格式为[movie_id,movie_name,movie_vote,movie_voter,movie_5star,movie_4star,movie_3star,movie_2star,movie_1star,movie_shortcom_num]
        self.path_film_info = "../comments/film_info.csv"
        # 存放短评csv文件的位置，数据格式为[movie_id,movie_title,comment_user,comment_time,comment_vote,comment_text]
        self.path_short_com = "../comments/short_comment/{}.csv"
        # 存放短评txt文件的位置，供jieba分词使用，分析完成后删除文件
        self.path_short_txt = "../comments/short_comment_txt/{}.txt"
        # 存放wordcloud生成图片的位置
        self.path_short_pic = "../comments/short_comment_pic/"

    '''
    返回电影id列表
    flag = 0, 文件来源为comments/film_info.csv
    flag = 1, 文件来源为most_pop_film.csv和most_score_film.csv
    '''

    def get_id_list(self, path, flag):
        id_list = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]:
                film_info = line.split(',')
                if flag:
                    film_id = film_info[-1][:-1]
                    film_title = film_info[0]
                else:
                    film_id = film_info[1]
                    film_title = film_info[2]
                id_list.append((film_id, film_title))
        return id_list

    '''
    读取film_info.csv文件，返回列表
    获得[movie_id,movie_name,movie_vote,movie_voter,movie_5-1star,movie_shortcom_num]
    '''

    def get_film_info(self):
        res_list = []
        with open(self.path_film_info, 'r', encoding='utf-8') as file:
            info_list = file.readlines()[1:]
            for info in info_list:
                res = info.split(',')
                res[-1] = res[-1][:-1]
                res_list.append(res)
        return res_list

    '''
    将存放短评的csv文件中的短评提取出来，转换为对应的txt文件，方便分词部分使用
    n=0 返回所有短评的str，不含分隔符
    n=1 返回短评列表
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
                line_len = len(lines)
                for line in lines:
                    t = line.split('$')[-1]
                    coms += (t + '$')
                    coms_list.append(t)
                coms += str(line_len)
            with open(txt_path, 'w', encoding='utf-8') as txt:
                txt.write(coms)
        else:
            with open(txt_path, 'r', encoding='utf-8') as txt:
                coms = txt.read()
                coms_list = coms.split('$')[:-1]
        # return coms_list if n else coms.replace('$', '')
        return coms_list if n else coms

    '''
    读取存放短评的csv文件，返回split过后的二维数组
    [movie_id,movie_title,comment_user,comment_time,comment_vote,comment_text]
    '''

    def com2list(self, film_id):
        com_path = self.path_short_com.format(film_id)
        coms_list = []
        if os.path.exists(com_path):
            with open(com_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]
                for line in lines:
                    coms = line.split('$')
                    coms_list.append(coms[1:])
        else:
            print("{}: file not exist".format(com_path))
        return coms_list

    '''    
    jieba分词，返回分词结果list
    '''

    def test_jieba_list(self, txt):
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

    # 计算len_score加权值，基于单部电影评论列表中评论长度排位（短评上限为350字）
    def cal_len_score(self, com_len):
        len_score = []
        for lr in com_len:
            if lr < 20:
                len_score.append(1)
            elif lr < 50:
                len_score.append(1.03)
            elif lr < 99:
                len_score.append(1.05)
            elif lr < 150:
                len_score.append(1.09)
            elif lr > 250:
                len_score.append(1.15)
            else:
                len_score.append(1)
        return len_score

    # 把vote的含%百分比str转换为小于1的小数
    def cal_vote(self, vote_list):
        res = []
        for vote in vote_list:
            vote = vote[:-1]
            n = float(vote)/100
            res.append(n)
        return res
    '''    
    文本情感期望型分析，基于snownlp库，分析影评的情感分数是否符合预期,计算公式见二期答辩ppt
    return: 列表，存储格式为(film_id, score_ex)的tuple
    '''

    def text_motion_nor(self):
        film_ids = []
        film_nor_score = []
        film_nlp_ex = []  # 电影评论平均nlp情感分数
        film_nlp_s1 = []
        film_nlp_s2 = []
        res_list = self.get_film_info()

        for info in res_list:
            # f_id, f_name, f_vote, f_voter, f_5star, f_4star, f_3star, f_2star, f_1star, f_scom_num = info[1], \
            #     info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10] 防止格式化
            f_id, f_name, f_vote, f_voter, f_5star, f_4star, f_3star, f_2star, f_1star, f_scom_num = info[1], \
                info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10]
            print("电影id: %s   电影名称: %s" % (f_id, f_name))
            t1 = 0.4  # 参数1
            t2 = 6  # 参数2
            sw_score = []  # 单条评论的nlp情感分数
            com_vote = []  # 单条评论的点赞数
            com_len = []  # 单条评论的长度
            total_com = int(f_scom_num)  # 电影总评论数
            total_vote = float(f_vote)  # 电影总评分

            # 获取每条评论的情感分数、点赞数、评论长度
            com_list = self.com2list(f_id)

            for com in com_list:
                sw = SnowNLP(com[5]).sentiments
                sw_score.append(sw)
                com_vote.append(float(com[4]))
                com_len.append(len(com[5]) - 1)

            len_score = self.cal_len_score(com_len)
            s1 = 0.0
            for i in range(len(com_list)):
                s1 += sw_score[i] * (1 + t1 * com_vote[i] / total_com) * len_score[i]

            s2 = total_vote / t2
            total_score = 0.8 * (s1 / len(sw_score) * 10) + 0.2 * s2
            if total_score > 10:
                total_score = 10
            print("Total expectation score: %f" % total_score)
            film_ids.append(f_id)
            film_nor_score.append(total_score)
            film_nlp_ex.append(sum(sw_score)/len(com_list))
            film_nlp_s1.append(s1)
            film_nlp_s2.append(s2)

        df = pd.DataFrame({
            "movie_id": film_ids,
            "movie_nor_score": film_nor_score,
            "nor_avg_swscore": film_nlp_ex,
            "s1": film_nlp_s1,
            "s2": film_nlp_s2
        })
        df.to_csv("../comments/film_nor_score.csv", encoding='utf-8')
        return 0


    '''    
    文本情感极端性分析，基于snownlp库，分析影评的情感分数是否极端化
    计算公式见二期答辩ppt
    return: 列表，存储格式为(film_id, score_ex)的tuple
    '''

    def text_motion_ex(self):
        film_ids = []
        film_vote = []
        film_ex_score = []
        film_comment_num = []  # 电影评论数
        film_nlp_ex = []
        film_vote_ex = []
        res_list = self.get_film_info()

        for info in res_list:
            # f_id, f_name, f_vote, f_voter, f_5star, f_4star, f_3star, f_2star, f_1star, f_scom_num = info[1], \
            #     info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10] 防止格式化
            f_id, f_name, f_vote, f_voter, f_5star, f_4star, f_3star, f_2star, f_1star, f_scom_num = info[1], \
                   info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10]
            print("电影id: %s   电影名称: %s" % (f_id, f_name))
            votes = [f_5star, f_4star, f_3star, f_2star, f_1star]
            votes_list = self.cal_vote(votes)

            t1, t2 = 0.8, 0.2
            sw_score = []  # 单条评论的nlp情感分数
            total_com = int(f_scom_num)  # 电影总评论数
            total_vote = float(f_vote)  # 电影总评分

            # 获取每条评论的情感分数、点赞数、评论长度
            com_list = self.com2list(f_id)
            for com in com_list:
                sw = SnowNLP(com[5]).sentiments
                sw_score.append(sw)

            sw_var = np.var(sw_score)  # 情感分数的方差
            vote_var = np.var(votes_list)  # 评分的方差

            total_score = t1 * sw_var + t2 * vote_var
            print("Total variance score: %f" % total_score)

            film_ids.append(f_id)
            film_vote.append(total_vote)
            film_ex_score.append(total_score)
            film_comment_num.append(total_com)
            film_nlp_ex.append(sw_var)
            film_vote_ex.append(vote_var)

        df = pd.DataFrame({
            "movie_id": film_ids,
            "movie_vote": film_vote,
            "movie_ex_score": film_ex_score,
            "movie_shortcom_num": film_comment_num,
            "movie_nlp_var": film_nlp_ex,
            "movie_vote_var": film_vote_ex
        })
        df.to_csv("../comments/film_ex_score.csv", encoding='utf-8')
        return 0

    # 主方法
    def run(self, args):
        assert len(args) != 0
        # 词频
        if args[0] == '0':
            pass
        # 情感趋向分析
        elif args[0] == '1':
            score_nor = self.text_motion_nor()
        # 情感极性分析
        elif args[0] == '2':
            score_ex = self.text_motion_ex()
        else:
            print("Invalid input of test code.")
        print("---------- Finish ----------")


if __name__ == '__main__':
    # 测试类型，0为分词和词云，1为情感分析
    # test_code = input("Test Num: ")
    # 可输入具体的电影id，不指定则输入0
    # test_f_id = input("Film id: ")
    ca = CommentAnalysis()
    ca.run('1')
