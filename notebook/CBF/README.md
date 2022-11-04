# CBF(Contents Based Filtering) - LDA model
CBF_LDA-Recommendation_for_books.ipynb
## 파일 설명
LDA 모델을 이용하여 CBF를 구현한 과정을 보여준다.
목차
1. Load Data
2. Tokenize
3. LDA
4. Model 선택
5. Recommender

### 1. Load Data
data/CBF 폴더에서 필요한 부분이 추출된 json파일들을 불러온다.  
각 파일들은 bookandlecture.json과 article.json에서 description 혹은 content column에서 정규표현식을 이용하여 tag등 내용과 관련 없는 context들을 한번 걸러낸 파일이다.

### 2. Tokenize
책의 description과 content의 내용을 형태소 분석기를 통해서 token화 시킨다.  
형태소 분석기를 통해 명사를 추출하도록 하였으며, 형태소 분석기는 Etri Api와 Mecab을 사용하였다.

#### 🛠 Mecab & Etri
|--|Mecab|Etri OpenApi|
|--|--|--|
|장점|속도가 빠르다.어절 분석에 강하다.|사전 학습된 형태소 사전을 통해 구어체 문어체를 가리지 않고 좋은 품질의 형태소 분석|

Mecab을 통해 뽑힌 총 단어 갯수 : 1190531,  
Mecab을 통해 뽑힌 유니크 단어 갯수 : 36096,  
Etri를 통해 뽑힌 총 단어 갯수 : 247481,  
Etri를 통해 뽑힌 유니크 단어 갯수 : 14554. 

Mecab을 통해서 추출한 형태소는 Etri에 비해 더 많은 단어(형태소)를 명사로 인식하여 뽑아 내었지만, 단어를 분절하는 형태에 가까워 의미없는 명사가 많이 포함되었다.    
반면 Etri는 Mecab에 비해 의미있는 명사들을 잘 뽑아내었지만, 여전히 사람이 평가하기에 의미가 없는 명사도 포함하고 있었다. 또한 의미를 지닌 형태소를 의미가 없다고 판단하여 버린 명사가 많아 토픽모델링에 어려움이 있었다.

이를 해결하기 위해 Mecab을 통해 description내용을 형태소별로 분절하고, 이 분절된 문장을 Etri를 통해 단어사전을 형성하였다.  

☞ 결과 : Mecab과 Etri 서로 다른 방식으로 추출한 형태소에서 교집합부분이 명사로 추출되어 핵심 단어들로 이루어진 단어 사전을 만들 수 있었다.  
사용된 단어 갯수 : 9025

### 3. LDA
CBF 모델링하는 방법으로 추출한 토큰을 바로 쓰기보다, 추출한 토큰을 가지고 토픽 모델링을 하고, 이 토픽을 통해 책 추천을 하기로 하였다.  
이를 도식화하면 다음과 같다.  
<code>Desciption</code> → <code>Tokenize</code> → <code>Topic Modeling</code> → <code>Recommend</code>

토픽을 뽑는 방법으로는 비교적 도메인을 덜 고려해도 되고, 자유도가 높은 LDA를 선택하여 토픽 모델링을 진행하였다.

### 4. Model 선택
그리드 서치를 통해 가장 적당한 hyperparameter를 찾은 결과, topic의 갯수는 35개가 가장 좋다고 판단함.

### 5. Recommender
책과 아티클에서 만들어낸 토픽 메트릭스에 코사인 유사도를 이용하여, 가장 비슷한 아이템을 찾아오는 함수를 구현하였다.  
아이템 이름을 넣고, 찾는 것이 book 인지 article인지 여부를 argument로 넣는다.  
함수가 동작하면 title에 넣은 아이템의 각 topic들에 대한 확률값을 불러온다.  
이 확률값을 가지고 코사인 유사도가 가장 높은 순으로 15개의 아이템을 불러오게 된다.
#### ☞ 책을 통해 책 뿐만이 아니라 아티클을 추천할 수 있게되고, 반대로 아티클에서 책을 추천하는 것도 가능해진다.

