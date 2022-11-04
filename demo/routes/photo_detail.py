from flask import Flask, Blueprint, render_template
from flask import request


import numpy as np
import pandas as pd
import warnings # 경고 메시지 무시
warnings.filterwarnings(action='ignore')
from tqdm import tqdm # 작업 프로세스 시각화
import re # 문자열 처리를 위한 정규표현식 패키지
from gensim import corpora # 단어 빈도수 계산 패키지
import gensim # LDA 모델 활용 목적
import pyLDAvis # LDA 시각화용 패키지
from collections import Counter # 단어 등장 횟수 카운트
from gensim.models.coherencemodel import CoherenceModel
import pickle
from gensim import corpora, models, similarities
# 한국어 형태소 분석기 중 성능이 가장 우수한 Mecab 사용
# from konlpy.tag import Mecab
# mecab = Mecab()
import os
project_folder = os.getcwd()
os.getcwd()
os.chdir('..')
os.chdir('..')
data_folder = os.getcwd()
print(data_folder)

bp = Blueprint('courses',__name__,url_prefix='/')

@bp.route('/photo-detail.html')
def result():
    name = request.args.get("name")

    # load data
    vectors = pd.read_json("/home/user_1/medistream-recsys-private/demo/static/data/final_tokens_2.json")
    df1 = pd.read_json('/home/user_1/medistream-recsys-private/demo/static/data/df_book_clean.json')
    df2 = pd.read_json('/home/user_1/medistream-recsys-private/demo/static/data/article_sum.json')

    df1 = df1.rename(columns={'_id':'id'})
    df_des = pd.concat([df1[['id','name_x','description']].rename(columns={'name_x':'title'}),df2[['id','title','content_tag_removed']].rename(columns={'content_tag_removed':'description'})], axis=0)
    df_des = df_des.reset_index().reset_index().rename(columns={'level_0':'문서 번호'})

    # Tokenize
    des_tokenized = []
    # for doc in tqdm(df_des['description']):
    #     tokens = [token for token in mecab.nouns(doc) if len(token) > 1] # 각 행(책,아티클)마다의 형태소 분석 명사 추출
    #     des_tokenized.append(tokens)
    with open('/home/user_1/medistream-recsys-private/demo/static/data/des_tokenized.pkl','rb') as f:
        des_tokenized = pickle.load(f)

    entri_token = []
    for doc in vectors['tokens']:
        entri_token.append(doc)

    from gensim import corpora
    dictionary = corpora.Dictionary(entri_token) # 명사 집합들 사전화
    corpus = [dictionary.doc2bow(text) for text in des_tokenized] # 각 문서마다 각 명사의 갯수 분석
    
    num_topics = 35
    lda_model_final = models.LdaModel.load('/home/user_1/medistream-recsys-private/data/CBF'+'/models6/ldamodels_bow_'+str(num_topics)+'.lda')
    corpus_lda_model = lda_model_final[corpus]
    index = similarities.MatrixSimilarity(lda_model_final[corpus])

    def book_recommender_book(title):
        books_checked = 0
        for i in range(len(df_des)):
            recommendation_scores = []
            # 넣은 타이틀이 동일할 경우
            if df_des.loc[i,'title'] == title:
                # i 번째 topic들 불러오기
                lda_vectors = corpus_lda_model[i]
                # 해당 토픽들 모임에 해당하는 similar matrix 값
                sims = index[lda_vectors]
                sims = list(enumerate(sims))
                for sim in sims:
                    book_num = sim[0]# enumerate index 값
                    recommendation_score = [df_des.iloc[book_num,2],df_des.iloc[book_num,3], sim[1]]
                    recommendation_scores.append(recommendation_score)
                
                recommendation_book = sorted(recommendation_scores[:373], key=lambda x: x[2], reverse=True) # sim score 값에 따라 정렬

                return recommendation_book
            
            else:
                books_checked +=1
            
            # 만약 for문을 다돌았는데 못찾았을 경우
            if books_checked == len(df_des): 
                book_suggestions = []
                print('Sorry, but it looks like "{}" is not available.'.format(title))

    recommendation_book = book_recommender_book(name)

    return render_template('photo-detail.html', name = name, recommendations = recommendation_book)

