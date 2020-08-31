# coding: utf-8

import csv
read_list = []

# 이곳에 입력할 csv 파일 주소 설정
f = open('./final.csv', 'r', encoding='UTF8')
reader = csv.DictReader(f)
import os
#websaver는 프로젝트 이름으로
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
import django
django.setup()
#pre_data는 새로 만든 앱 이름 프로젝트 안에 모델을 만들수없으니 앱 하나 만들고 시작할것
#MovieData 는 models에서 만든 모델 이름
from pre_data.models import MovieData
#row['i'] 처럼 csv파일 제일 상위에 만들어놓은 분류를 그대로적을것
if __name__=='__main__':
    for row in reader:
        MovieData(movie_id = row['i'], title = row['title'], star = row['star'], movie_rating = row['movie_rating'], genre = row['genre'], director = row['director'], actors = row['actors'], summary = row['summary']).save()
        print(row['title'] + 'is saved!')
