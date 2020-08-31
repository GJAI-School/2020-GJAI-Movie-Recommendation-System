import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import re

page_dic = {'1990': 17, '1991' : 16, '1992' : 20, '1993': 21, '1994' : 19, '1995' : 17, '1996' : 17, '1997' : 17, '1998' : 15, '1999' : 16, 
            '2000' : 19, '2001' : 17, '2002' : 18, '2003' : 20, '2004' : 38, '2005' : 21, '2006' : 24, '2007' : 26, '2008' : 28, '2009' : 24,
            '2010' : 29, '2011' : 41, '2012' : 44, '2013' : 61, '2014' : 76, '2015' : 71, '2016' : 59, '2017' : 53, '2018' : 50, '2019' : 43,
            '2020' : 30}

def load_soup(dic):
    years = list(dic.keys())
    pages = list(dic.values())

    soup_object = []
    for idx, year in enumerate(years): 
        for page in range(1, pages[idx]+1):
            # print(year ,page)
            base_url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open={year}&page={str(page)}"
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            data_select = soup.select("#old_content > ul > li")
            soup_object.append(data_select)
    return soup_object

def load_movie_id(dic):
    movie_id = []

    for movie_select in load_soup(dic):
        # print(movie_select)
        for data in movie_select:
            movie_id.append(data.select_one('a')['href'].split('=')[1])
    return movie_id

def load_url(subject, movie_num):
    base_url = f'https://movie.naver.com/movie/bi/mi/{subject}.nhn?code={movie_num}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.select_one('#content > div.article')
    return article

page_dic2 = {'1990': 17, '1991' : 16}
movie_id = load_movie_id(page_dic)
# print(movie_id)
print(len(movie_id))

for idx, movie_num in enumerate(movie_id):
    # print(idx+1)
    basic_article = load_url('basic', movie_num) # 줄거리를 보여주는 페이지
    datail_article = load_url('detail', movie_num) # 출연배우를 보여주는 페이지

    # 19 청불영화에 대한 예외처리
    if basic_article is None:
        continue
    
    # 영화제목
    title = basic_article.select_one('div.mv_info_area > div.mv_info > h3').get_text().replace('\n', '')
    # print(title)

    # 네티즌 점수 
    star_lst = []
    for num in range(1,5):
        if basic_article.select_one(f'div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score > a > em:nth-of-type({num})') is not None:
            star = basic_article.select_one(f'div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score > a > em:nth-of-type({num})').get_text()
            star_lst.append(str(star))
    # print("".join(i for i in star_lst))

    # 영화 정보리스트
    info_lst = [i.get_text() for i in basic_article.select('div.mv_info_area > div.mv_info > dl > dt')]
    # print(info_lst)

    # 영화 장르
    if '개요()' in info_lst:
        idx = info_lst.index('개요()')
        genre = [i.get_text() for i in basic_article.select(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type({idx+1}) > p > span:nth-of-type(1) > a')]
    else:
        genre = ""
    # print(genre)

    # 영화 감독
    if '감독' in info_lst:
        idx = info_lst.index('감독')
        if basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type({idx+1}) > p > a') is not None:
            movie_director = basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type({idx+1}) > p > a').get_text()
    else:
        movie_director = ""
    # print(movie_director)

    # 영화 등급
    if '등급' in info_lst:
        idx = info_lst.index('등급')
        movie_rating = basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type({idx+1}) > p > a').get_text()
    else:
        movie_rating = ""
    # print(movie_rating)

    # 영화 출연
    movie_actors = datail_article.select('div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100')
    #content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100
    actor_lst = []

    # 영화배우 count
    actor_counts = datail_article.select('div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')
    actor_counts = len(actor_counts)

    for actors in movie_actors:
        for num in range(1, actor_counts+1):
            if actors.select_one(f'ul > li:nth-of-type({num}) > div > div > p.in_prt > em').get_text() == '주연':
                if actors.select_one(f'ul > li:nth-of-type({num}) > div > a') is not None:
                    actor = actors.select_one(f'ul > li:nth-of-type({num}) > div > a').get_text()
                    actor_lst.append(actor)
                elif actors.select_one(f'ul > li:nth-of-type({num}) > div > span') is not None:
                    actor = actors.select_one(f'ul > li:nth-of-type({num}) > div > span').get_text()
                    actor_lst.append(actor)
            else:
                break
            
    # 영화 줄거리
    if basic_article.select_one('div.section_group.section_group_frst > div:nth-of-type(1) > div > div > div > h4') is None:
        summary = ""
    else:
        summary = basic_article.select_one('div.section_group.section_group_frst > div:nth-of-type(1) > div > div.story_area > p').get_text().replace('\r', "").replace('\xa0', "")
    # print(summary)

    movie_data = {
        'movie_id' : movie_num,
        'title' : title,
        'star' : "".join(i for i in star_lst),
        'movie_rating' : movie_rating,
        'genre' : genre,
        'director' : movie_director,
        'actors' : actor_lst,
        'summary' : summary
    }

    # print(movie_data, '\n')

    with open('./movie_data2.csv', 'a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['movie_id', 'title', 'star', 'movie_rating',  'genre', 'director', 'actors', 'summary']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerow(movie_data)
