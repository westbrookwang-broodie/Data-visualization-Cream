# 整合most_pop_film和most_score_film的文件到一个csv文件中,方便后续读取
pop_path = "most_pop_film/S{}.csv"
score_path = "most_score_film/高分{}.csv"

pop_list = []
score_list = []
for i in range(1, 11):
    pop_list.append(pop_path.format(str(i)))
    score_list.append(score_path.format(str(i)))

pop_path = "most_pop_film.csv"
score_path = "most_score_film.csv"

pop_t = ''
score_t = ''

flag = 1
for path in pop_list:
    with open(path, 'r', encoding='utf-8') as file1:
        pop = file1.readlines()
        if flag:
            pop_t += pop[0]
            flag = 0
        for j in range(1, len(pop)):
            pop_t += pop[j]
    file1.close()

flag = 1
for path in score_list:
    with open(path, 'r', encoding='utf-8') as file2:
        pop = file2.readlines()
        if flag:
            score_t += pop[0]
            flag = 0
        for j in range(1, len(pop)):
            score_t += pop[j]
    file2.close()

with open(pop_path, 'w', encoding='utf-8') as t:
    t.write(pop_t)

with open(score_path,'w',encoding='utf-8') as t:
    t.write(score_t)



