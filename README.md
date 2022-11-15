# 메디스트림 기업 과제
## 🔥 기업 소개
- 전국 한의사 62%가 가입한 한의사를 위한 폐쇄형 커머스 플랫폼 서비스
- 커뮤니티, 커머스, 클래스, 경영지원 등의 서비스 제공
- [기업 홈페이지](https://auth.medistream.co.kr/login?client_id=01FWFWVMHNSPW7D5PE8WY6R6H2&redirect_uri=https://medistream.co.kr/auth?redirect=Lw%3D%3D&response_type=code)

## 🥸 기업 요청
```
- 도서 카테고리에 대한 추천
- 도서는 인기있는 상품이 주로 판매되고 있고, 다양한 상품이 추천될 수 있도록   
 추천 시스템을 시도해보았지만 most popular만 추천이 되는 문제가 반복되어 다양성이 충족된 추천이 되길 원함
- 또한, 도서 및 아티클 메타 정보 활용을 통한 추천을 원함
```

## 📌 프로젝트 목표
- 다양한 상품을 추천하여 판매되는 상품의 종류를 넓히는 것 목표
- 유저 행동 기반으로 학습을 하며 다양한 추천이 가능하도록 CF 기반 추천 구현
- 도서 및 아티클 메타 정보를 활용한 CBF 추천 구현

## 📅 프로젝트 수행 기간 
- 2022.09.05 ~ 2022.10.23

## 🙌 팀원 소개

|  [박영수](https://github.com/y001003)     |  [이세현](https://github.com/qsdcfd)    |   [정혜빈](https://github.com/HYEBINess)          |   [최진수](https://github.com/jinsuc28)  | 
| :-----------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------: | 
| [![Avatar](https://avatars.githubusercontent.com/u/68417368?v=4)](https://github.com/y001003) | [![Avatar](https://avatars.githubusercontent.com/u/86671456?v=4)](https://github.com/qsdcfd) | [![Avatar](https://avatars.githubusercontent.com/u/97460313?v=4)](https://github.com/HYEBINess) | [![Avatar](https://avatars.githubusercontent.com/u/86936634?v=4)](https://github.com/jinsuc28) | 

## 협업 방법
- 폐쇄형 플랫폼이기 때문에 데이터 보안 문제로 GCP 서버를 통해서만 작업을 진행
- GCP 서버를 이용하여 각 팀원 별 공간을 할당하였으며 base로 jupyter notebook 환경에서 작업을 진행
- Jira Confulence 및 github project 이용하여 작업 공유 및 협업 진행
- [Confulence](https://zepellin.atlassian.net/wiki/spaces/1515/pages) ,[Github Project](https://github.com/orgs/Recommend-System-15/projects/1/views/2) 

## 사양
- Disk 200g, Rem 64g, 8 core Intel(R) Xeon(R) CPU @ 2.20GHz, Ubuntu 18.04.6 LTS

# 📁 데이터

<img width="572" alt="order 데이터" src="https://user-images.githubusercontent.com/86936634/199991521-08c3d26f-d514-426d-aa4d-ae91d6f894ab.png">

- 전체 아이템 중 '도서' 구매 데이터만 사용
- 구매 데이터 중에서도 paid가 완료되고, cancelled 되지 않은 '완전한' 구매 기록만 사용
- 모델 학습에 있어서 비교적 적은 데이터임을 확인
- CF 모델 학습하는데 사용

<img width="605" alt="article book 데이터" src="https://user-images.githubusercontent.com/86936634/199992682-2c569c6e-eb27-46be-b9fc-383e1982f23a.png">

- Article : 메디스트림 상품 리뷰 및 커뮤니티 글
- Book : 도서의 context 한 메타 정보
- CBF 모델 학습하는데 사용

# CF 모델
- 비슷한 성향을 갖는 다른 유저가 좋아한 아이템을 현재 유저에게 추천하는 방법
- 적은 데이터와 콜드스타트 유저에 대해서도 학습이 가능하다는 점에서 MF, LMF, MP 모델을 선택   

## 1) Train 데이터 기간 설정
- 일반적으로 추천시스템에서 train 데이터 기간으로 3개월 정도를 보편적으로 적용하여 학습히지만,   
메디스트림 order 데이터 수는 매우 적으며 유저와 아이템 interaction 기간도 일반적이지 않고 매우 길어    
일반적인 추천시스템 train data 기간과는 달라야한다고 판단
- train test 기간을 1,2,3,4,6개월을 각각 모두 blocking 방식의 CV 를 사용하여서 평가를 진행
- MF, LMF 모델 기준으로 NDCG@100 성능이 좋으며 일정한 성능을 유지하는 학습기간을 최종 train data 기간으로 설정
- 최종적으로 train 5개월을 학습기간으로 최종 선정
- 링크 참조 ([실험 및 평가 결과](https://docs.google.com/spreadsheets/d/1Y_YDjP-QcCq7Qfgk2Cr0epKyX_6Fk4Eel1oklIJLLfE/edit#gid=822503154))

## 2) Train Test split
<img width="510" alt="Train Test split" src="https://user-images.githubusercontent.com/86936634/200008140-fd1caef9-5631-4315-bc9f-dee30a1cfe16.png">

- 유저가 마지막 3주 동안 구매한 도서 아이템을 예측 task
- train, valid, test 나누어 모델 하이퍼파라미터 튜닝 및 평가

## 3) Base Model 선정
- Base Model로 메디마켓에서 진행 중인 연관추천(인기순,최신순,오래된순,높은가격순,낮은가격순,이름순 총6가지) 선정 이와 학습 모델 성능 비교

<img width="750" alt="Base Model 선정" src="https://user-images.githubusercontent.com/86936634/200018770-e37ff2ff-b24f-48d0-932a-73b48811c870.png">

- Base Model 경우 실제 메디마켓에서 진행되는 추천 상황을 반영 위해 전체 데이터 사용
- Our Model 경우 최근 5개월 데이터를 사용하여 학습 및 예측 진행

## 4) 평가지표
<img width="750" alt="평가지표" src="https://user-images.githubusercontent.com/86936634/200016021-31e7768a-bf74-4cf1-bb03-68e0a408c826.png">

- 모델 성능 비교를 위해 예측 개수를 지정함 그 방법으로 메디마켓 메인 페이지에 처음 노출되는 아이템 수를 고려
- 실제 메디마켓 배너를 클릭했을 때 유저가 처음 노출되는 아이템 개수가 15 개인 것을 확인 따라서 모델을 통해   
노출될 상위 15개의 아이템 뽑고 각 지표를 통해 평가를 진행

## 5) 최종 결과

|model| NDCG@15 | entropy@15 |
|---|-------|--------:|
|Ensemble| 0.06151| 3.33082 |  
|base-model-MP| 0.06126| 2.70805 |
|MF| 0.0530| 3.3352 |
|LMF| 0.0542| 3.5511 |

- base model 중 가장 점수가 높았던 Most Popular 과 비교
- MF, LMF 는 NDCG 점수가 base-model-mp 비해 낮지만 entropy 점수가 높음
- LMF(predict@12) 와 base-model-mp(top3) 앙상블 진행
- base-model-mp 대비 앙상블 모델이 가장 높은 NDCG 점수와 entropy 점수 분포를 보여 성능 개선 확인

## 6) 적용 방안
<img width="650" alt="추천순" src="https://user-images.githubusercontent.com/86936634/200104839-a80d111e-3ea7-4d59-9f8b-2d6c0a596177.png">

- 메디 마켓 추천순 버튼을 만들고 유저가 클릭시 행동기반 추천 진행
- MF 모델 기반 다양한 유저에게 개인화 및 다양한 상품 추천

# CBF 모델
- 콘텐츠 기반 추천으로 각 아이템 간 context 정보를 유사도 기반으로 추천하는 방법
- Article, Book 의 메타 데이터를 통해 형태소 분석 및 LDA 토픽 모델 기반으로 한 유사한 도서 및 Article 추천

## 1) 데이터 전처리
<img width="550" alt="데이터 전처리" src="https://user-images.githubusercontent.com/86936634/200101991-ca368110-1bc1-43e8-b33b-a49f434b738b.png">

||Mecab|Etri OpenApi|
|--|--|--|
|장점|속도가 빠르다.어절 분석에 강하다.|사전 학습된 형태소 사전을 통해 구어체 문어체를 가리지 않고 좋은 품질의 형태소 분석  *링크 참조 ([etri](https://github.com/Recommend-System-15/medistream-recsys/tree/main/notebook/CBF/etri))|

- 위 사진과 같이 두가지 형태소 분석기 모두 이용하여 형태소 추출시 좀더 핵심 단어만 추출
- Mecab을 통해서 추출한 형태소는 Etri에 비해 더 많은 단어(형태소)를 명사로 인식하여 뽑아 내었지만, 단어를 분절하는 형태에 가까워 의미없는 명사가 생성됨    
반면, Etri는 Mecab에 비해 의미있는 명사들을 잘 뽑아내었지만, 여전히 의미가 없는 명사도 포함하고 있었음.   
또한, 의미를 지닌 형태소를 의미가 없다고 판단하여 버린 명사가 많아 토픽모델링에 어려움 발생
- Mecab 명사 추출, ETRI 단어 사전 생성 이후 통해 Tfidf 진행하여 도서 및 아티클 별 임베딩 생성

## 2) LDA 토픽 모델 선정 이유 및 학습 방법
- 토픽 모델링 종류로는 LSA, LDA 두가지 존재
- LSA 경우 문맥을 반영한 토픽 모델링이며 LDA는 확률기반 토픽 모델링이기 때문에 한의학 도메인 정보를 잘 표현하기 위해서는 LDA 사용하는 것이 좋다고 판단
- Coherence Score 와 Perplexity Score를 사용하여 토픽 개수를 선정하였으며 35개의 주제 선택하여 학습 진행

## 3) 추천 방법
<img width="800" alt="CBF 추천 방법" src="https://user-images.githubusercontent.com/86936634/200102420-5367f35d-6c9d-4faa-a6d6-cf346b838c21.png">

- Tfidf 임베딩 데이터를 LDA 토픽 모델에 넣으며 각 도서 및 아티클 별 35개 토픽 중 확률 값 생성
- 각 도서 및 아티클은 상위 10개의 토픽을 뽑게 되며 이를 통해 row 는 도서, 아티클은 column 으로 토픽 matrix 생성되며 코사인 유사도 기반 matrix 새로 생성됨
- 이를 기반으로 비슷한 아티클, 혹은 도서 추천 진행

## 4) 적용 방안
<img width="500" height="200" alt="CBF 적용 방법" src="https://user-images.githubusercontent.com/86936634/200104715-b9a8df99-c029-470f-bab8-d33ba21727fa.png">

- 유저가 아티클 혹은 도서 페이지 방문시 관련 도서 또는 아티클이 나오는 배너를 만들어 추천 진행

# 기대 효과
<img width="589" alt="최종 기대 효과" src="https://user-images.githubusercontent.com/86936634/199998364-79b02dcc-3fcf-4abc-8e6b-cb3f361fb17f.png">


## 🛠️ Structure
```
medistream-recsys
├── LICENSE
├── README.md
├── 📁 data❗(private)
│   ├── 📁 CBF
│   │   ├── 💾 article_sum.json
│   │   ├── 💾 book_categorize.csv
│   │   ├── 💾 category_concat.json
│   │   ├── 💾 des_tokenized.pkl
│   │   ├── 💾 df_book_clean.json
│   │   ├── 💾 final_tokens_2.json
│   ├── 💾 products.json
│   └── 💾 select_column_version_4.json
├── 📁 models
│   ├── 📁 CBF
│   │   ├── 💾 README.md
│   │   └── 💾 cbf_module.py
│   ├── 📁 CF
│   │   ├── 💾 README.md
│   │   ├── 💾 MF-model.ipynb
│   │   ├── 💾 dataload.py
│   │   ├── 💾 evaluation.py
│   │   ├── 💾 model.py
│   │   ├── 💾 predict_list.csv
│   │   ├── 💾 preprocess.py
│   │   └── 💾 utils.py
│   └── 💾 README.md
├── 📁 notebook
│   ├── 📁 CBF
│   │   ├── 💾 README.md
│   │   ├── 💾 CBF_LDA-Recommendation_for_books.ipynb
│   │   └── 📁 etri
│   │       ├── 💾 README.md
│   │       ├── 💾 erti_articles_tokens.ipynb
│   │       └── 💾 etri_book_tokens.ipynb
│   ├── 📁 CF
│   │   ├── 💾 README.md
│   │   ├── 💾 1-valid-evaluation-and-hyperparameter-tuning.ipynb
│   │   ├── 💾 2-CV-check-consistency.ipynb
│   │   ├── 💾 3-evaluation.ipynb
│   │   └── 📁 predict-100-find-train-date
│   │       └──⋮
│   ├── 📁 EDA
│   │   ├── 💾 Apriori 연관 분석.ipynb
│   │   ├── 💾 article_EDA.ipynb
│   │   └── 💾 order_data_EDA.ipynb
│   └── 💾 README.md
└── 📁 util
│   └── 💾 utils.py
└── 💾 requirements.txt
```

## 📜 상세 설명
### 1. EDA

- [EDA ](./notebook/EDA/)
- [CF ](./notebook/CF/README.md)
- [CBF](./notebook/CBF/README.md)

### 2. Model

- [CF Model README](./models/CF/README.md)
- [CBF Model README](./models/CBF/README.md)

## 📦 사용 라이브러리
- [requirements.txt](requirements.txt)

## ✨ 프로젝트 산출물
- [최종 발표 자료](https://github.com/Recommend-System-15/medistream-recsys/files/9946007/15.Medistream.pdf)
