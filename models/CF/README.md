# CF (Collaborative Filtering)
<font size=3>**최종 선택된 Ensemble (LMF & base model MP MIX) 모델 모듈화**</font>   

## 산출물 설명

**[MF-model.ipynb](MF-model.ipynb)**   
- MF,LMF,MP, 메디마켓 연관추천 base model 및 최종 ensemble 학습 결과 및 주석 저장된 파일

**[dataload.py](dataload.py)**   
- order data 와 product data 불러오며 간단한 기간 전처리를 진행

**[evaluation.py](evaluation.py)**   
- NDCG, Entropy Diversity 평가지표 클래스 관련한 파일
- 정확한 순위 예측과 다양한 아이템 추천 성능 평가 위해 두가지 평가지 선택

**[model.py](model.py)**
- 최종적으로 선택된 ensemble(LMF & base model MP MIX)로 모델 학습 및 산출물 생성 파일

**[preprocess.py](preprocess.py)**
- 프로모션 데이터 전처리 및 train test split 등과 같은 전처리 진행

**[utils.py](utils.py)**
- 관련 라이브러리 및 함수가 있는 util 파일

**[predict_list.csv](predict_list.csv)**
- ensemble 결과 추천된 15개 아이템 결과가 저장
- csv 형식으로 유저와 아이템 id 식별 코드 정보가 들어가 있습니다.

## 최종 결과

- base model 중 가장 점수가 높았던 Most Popular 과 비교

|model| NDCG@15 | entropy@15 |
|---|-------|--------:|
|Ensemble| 0.06151| 3.33082 |  
|base-model-MP| 0.06126| 2.70805 |

## 실행방법

- order data와 product 파일 path와 결과 csv 저장 경로를 입력 후 실행
```
python3 model.py --order_path --product_path --result_download_path
```
