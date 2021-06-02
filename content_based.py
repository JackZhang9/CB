#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/6/1 15:27
# @Author : CN-JackZhang
# @File: content_based.py
import operator
from utility import read
'''用户刻画，内容推荐'''

def get_time_score(timestamp):
    '''

    :param timestamp:input timestamp
    :return: time score
    '''
    fix_time_stamp = 1476086345
    tatal_sec = 24*60*60
    delta = (fix_time_stamp - timestamp)/tatal_sec/100
    return round(1/(1+delta), 3)


def get_up(movie_cate, input_file):
    '''
    得到用户刻画
    :param movie_cate:key movieid, value dict,key category value ratio
    :param input_file:user rating file
    :return:dict, key userid, value [(category,ratio),(category1,ratio1)]
    '''
    line_num = 0
    record = {}
    up = {}
    with open(input_file) as fp:
        for line in fp:
            if line_num == 0:
                line_num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userId, movieId, rating, timestamp = item[0], item[1], float(item[2]), int(item[3])
            if rating < 4.0:
                continue
            #movieid不在，无法获取到类别
            if movieId not in movie_cate:
                continue
            time_score = get_time_score(timestamp)
            if userId not in record:
                record[userId] = {}
            for fix_cate in movie_cate[movieId]:
                if fix_cate not in record[userId]:
                    record[userId][fix_cate] = 0
                record[userId][fix_cate] += rating*time_score*movie_cate[movieId][fix_cate]
        fp.close()
    for userId in record:
        if userId not in up:
            up[userId] = []
        toatl_score = 0
        for zuhe in sorted(record[userId].items(),key=operator.itemgetter(1),reverse=True)[:2]:
            up[userId].append((zuhe[0], zuhe[1]))
            toatl_score += zuhe[1]
        for index in range(len(up[userId])):
            up[userId][index] = (up[userId][index][0], round(up[userId][index][1]/toatl_score, 3))
    return up

def recom(cate_movie_sort,up,userId,topk=10):
    '''
    得到推荐结果
    :param cate_movie_sort:倒排
    :param up:用户偏好
    :param userId:
    :param topk:推荐个数
    :return:dict, key userid,value [movieid1,movieid2]
    '''
    recom_result = {}
    if userId not in recom_result:
        recom_result[userId] = []
    for zuhe in up[userId]:
        cate = zuhe[0]
        ratio = zuhe[1]
        num = int(topk*ratio) + 1
        if cate not in cate_movie_sort:
            continue
        recom_list = cate_movie_sort[cate][:num]
        recom_result[userId] += recom_list
    return recom_result

def run_main():
    ave_score = read.get_ave_score('../data/ratings.txt')
    movie_cate, cate_movie_sort = read.get_movie_cate(ave_score, '../data/movies.txt')
    #得到所有用户的刻画
    up = get_up(movie_cate, '../data/ratings.txt')
    # print(len(up), up['1'], recom(cate_movie_sort, up, '1'))
    '''
    100 [('Drama', 0.6), ('Action', 0.4)] {'1': ['30', '149', '156', '178', '279', '280', '290', '611', '667', '1224', '2344', '2826']}
    '''
if __name__ == '__main__':
    run_main()