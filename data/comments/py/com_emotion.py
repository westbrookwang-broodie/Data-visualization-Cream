from snownlp import SnowNLP
import os

'''
    几个测试用例的film_id:
    30282387 银河补习班
    1424552 大决战之辽沈战役
    11510624 全民目击
'''

# 可输入具体的电影id，不指定则输入0
test_f_id = input("Film id: ")
info_sw = "第{}条评论的情感分数是: {}"

file_path = "../comments/short_comment/{}.csv".format(test_f_id)
if os.path.exists(file_path):
    total_score = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[1:]
        com_len = len(lines)

        for line in lines:
            coms = line.split('$')
            com_id = coms[0]
            com_sc = coms[-2]
            com_text = coms[-1]
            sw = SnowNLP(com_text).sentiments

            # print(info_sw.format(com_id, sw))

