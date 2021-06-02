#!/usr/bin/env python
# _*_coding: utf-8 _*_
# @Time : 2021/5/25 20:42
# @Author : CN-JackZhang
# @File: read.py
import operator

def get_ave_score(input_file):
    '''
    得到电影的平均评分
    :param input_file:用户评分文件
    :return:一个字典，key: movieid value:ave_score
    '''
    line_num = 0
    record = {}
    ave_score = {}
    with open(input_file) as fp:
        for line in fp:
            if line_num == 0:
                line_num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userId, movieId, rating = item[0], item[1], float(item[2])
            if movieId not in record:
                record[movieId] = [0, 0]
            record[movieId][0] += rating
            record[movieId][1] += 1
        fp.close()
        for movieId in record:
            ave_score[movieId] = round(record[movieId][0]/record[movieId][1], 3)
        return ave_score

def get_movie_cate(ave_score, input_file):
    '''
    获得movie的类别，每一个类别对应的所有movie，按照平均得分的倒排
    :param ave_score:一个字典，key movieid, value rating score
    :param input_file:movie info file
    :return:a dict，key movieid,value a dict,key cate, value ratio
            a dict,key cate, value [movieid1, movieid2, movieid3]
    '''
    line_num = 0
    movie_cate = {}
    record = {}
    cate_movie_sort = {}
    with open(input_file) as fp:
        for line in fp:
            if line_num == 0:
                line_num += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            movieid, cate = item[0], item[-1]
            cate_list = cate.strip().split('|')
            ratio = round(1/len(cate_list),3)
            if movieid not in movie_cate:
                movie_cate[movieid] = {}
            for fix_cate in cate_list:
                movie_cate[movieid][fix_cate] = ratio
        fp.close()
    for movieid in movie_cate:
        for cate in movie_cate[movieid]:
            if cate not in record:
                record[cate] = {}
            movieid_rating_score = ave_score.get(movieid,0)
            record[cate][movieid] = movieid_rating_score
    for cate in record:
        if cate not in cate_movie_sort:
            cate_movie_sort[cate] = []
        for zuhe in sorted(record[cate].items(),key=operator.itemgetter(1), reverse=True)[:100]:
            cate_movie_sort[cate].append(zuhe[0])
    return movie_cate, cate_movie_sort


# if __name__ == '__main__':
    a_s=get_ave_score('../data/ratings.txt')
    # print(len(a_s), a_s['31'])
    # movie_cate, cate_movie_sort = get_movie_cate(a_s, '../data/movies.txt')
    # print(movie_cate['1'], '\n', cate_movie_sort['Children'])