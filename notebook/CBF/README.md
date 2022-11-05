# CBF(Contents Based Filtering) - LDA model

## ipynb 파일 세부 설명
LDA 모델을 이용하여 CBF를 구현한 과정 및 세부 설명

## 목차
1. Load Data
2. Tokenize
3. LDA
4. Model 선택
5. Recommender

### 1. Load Data
- data/CBF 폴더에서 필요한 부분이 추출된 json파일 로드  
- 각 파일들은 bookandlecture.json과 article.json에서 description 혹은 content column에서 정규표현식을 이용하여 tag 등 내용과 관련 없는 context들을 한번 걸러낸 파일

### 2. Tokenize
- 도서의 description과 content의 내용을 형태소 분석기를 통해서 token화
- 형태소 분석기를 통해 명사를 추출하도록 하였으며, 형태소 분석기는 Etri Api와 Mecab을 사용

#### Mecab & Etri 형태소 분석기
||Mecab|Etri OpenApi|
|--|--|--|
|장점|속도가 빠르며 어절 분석에 강함|사전 학습된 형태소 사전을 통해 구어체 문어체를 가리지 않고 좋은 품질의 형태소 분석|
| 뽑힌 단어 개수 |1,190,531     |247,481|
| 뽑힌 유니크 단어 개수 | 36,096    |14,554|

- Mecab을 통해서 추출한 형태소는 Etri에 비해 더 많은 단어(형태소)를 명사로 인식하여 뽑아 내었지만, 단어를 분절하는 형태에 가까워 의미없는 명사가 많이 포함됨 확인   
- 반면, Etri는 Mecab에 비해 의미있는 명사들을 잘 뽑아내었지만, 여전히 사람이 평가하기에 의미가 없는 명사도 포함
- 또한, 의미를 지닌 형태소를 의미가 없다고 판단하여 버린 명사가 많아 유의미한 토픽 모델링에 어려움 확인
- 이를 해결하기 위해 Mecab을 통해 description내용을 형태소 별로 분절하고, 이 분절된 문장을 Etri를 통해 단어사전을 형성  

☞ 결과 : Mecab과 Etri 서로 다른 방식으로 추출한 형태소에서 교집합부분이 명사로 추출되어 핵심 단어들로 이루어진 단어 사전 구축
사용된 단어 갯수 : 9025
- 이를 기반으로 도서와 아티클의 Tfidf 임베딩을 생성

### 3. LDA
- 토픽을 생성 모델로는 비교적 도메인을 덜 고려해도 되고, 자유도가 높은 LDA를 선택하여 토픽 모델링을 진행하였다.
- Tfidf 임베딩 데이터를 LDA 토픽 모델에 넣으며 각 도서 및 아티클 별 35개 토픽 중 확률 값 생성
- 각 도서 및 아티클은 상위 10개의 토픽을 뽑게 되며 이를 통해 row 는 도서, 아티클은 column 으로 토픽 matrix 생성되며 코사인 유사도 기반 matrix 새로 생성됨
- 이를 기반으로 비슷한 아티클, 혹은 도서 추천 진행
- 지금까지 과정을 크게 도식화하면 다음과 같다.  
<code>Desciption</code> → <code>Tokenize</code> → <code>Topic Modeling</code> → <code>Recommend</code>

### 4. Model 선택
- Coherence Score 와 Perplexity Score를 비교하며 토픽 개수를 선정하였으며 35개의 주제 선택하여 학습 진행

### 5. Recommender
- 도서와 아티클에서 만들어낸 토픽 matrix를 코사인 유사도를 이용하여, 가장 비슷한 아이템을 찾아오는 함수를 구현  
1. 아이템 이름을 넣고, 찾는 것이 book 인지 article인지 여부를 argument로 넣기 
2. 함수가 동작하면 title에 넣은 아이템의 각 topic들에 대한 확률값을 불러오기  
3. 이 확률값을 가지고 코사인 유사도가 가장 높은 순으로 15개의 아이템 추천 진행

#### ☞ 도서를 통해 도서 뿐만이 아니라 아티클을 추천할 수 있으며, 반대로 아티클에서 도서를 추천하는 것도 가능

