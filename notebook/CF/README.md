# CF Model 실험 및 평가
<font size=3>**CF 모델 실험 및 평가 결과에 대해 정리합니다.**</font>   
- 관련 결과 링크 참조 ([실험 및 평가 결과](https://docs.google.com/spreadsheets/d/1Y_YDjP-QcCq7Qfgk2Cr0epKyX_6Fk4Eel1oklIJLLfE/edit#gid=822503154))

# 데이터 학습 기간 실험
## **[predict-100-find-train-date](./predict-100-find-train-date)**
```
- 일반적으로 추천시스템에서 train 데이터 기간으로 3개월 정도를 보편적으로 적용하여 학습히지만,   
메디스트림 order 데이터 수는 매우 적으며 유저와 아이템 interaction 기간도 일반적이지 않고 매우 길어    
일반적인 추천시스템 train data 기간과는 달라야한다고 판단
- train test 기간을 1,2,3,4,6개월을 각각 모두 blocking 방식의 CV 를 사용하여서 평가를 진행
- MF, LMF 모델 기준으로 NDCG@100 성능이 좋으며 일정한 성능을 유지하는 학습기간을 최종 train data 기간으로 설정
- 최종적으로 train 5개월을 학습기간으로 선정
```
# CF model 실험 및 평가 진행
## **[1-valid-evaluation-and-hyperparameter-tuning](./1-valid-evaluation-and-hyperparameter-tuning.ipynb)**
```
- train(04.13 ~ 08.01 (약 5개월)) , valid(08.02 ~ 08.22 (약 3주)), test(08.23 ~ 09.13 (약 3주))    
나누고 valid 대한 성능 비교 및 하이퍼파라미터 튜닝 진행
- 적은 데이터와 콜드스타트 유저에 대해서도 학습이 가능하다는 점에서 MF, LMF, MP 모델을 선택하였으며   
base-model로 메디마켓에서 진행 중인 연관추천(인기순,최신순,오래된순,높은가격순,낮은가격순,이름순 총6가지)을    
선정하였으며 비교하여 평가 진행 예정
- 평가지표로 NDCG 와 Entropy 점수로 평가를 진행합니다. NDCG는 아이템 예측 정확도와 순위까지 평가를 진행하며    
entropy 점수의 경우 메디스트림에서 요청한 다양성 정도를 비교할 수 있는 평가지표
- predict item 개수는 15개로 메디마켓 메인 페이지를 들어갔을 때 유저에게 처음 노출되는 아이템 개수가 15개인 것으로 확인   
따라서 유저가 받게될 실제 추천 상황을 반영하기 위해서 NDCG@15, entropy@15 로 평가 진행
```

## **[2-CV-check-consistency](./2-CV-check-consistency.ipynb)**
```
- MF, LMF, MP 및 앙상블 모델의 정합성을 테스트하기 위해서    
time series CV 방식 중 blocking 방식을 통해서 검증을 수행
```

## **[3-evaluation](./3-evaluation.ipynb)**
```
- 최종적으로 base-model 과 MF,LMF,MP,ensemble 성능을 비교
```

# 최종 결과
- base model 중 가장 점수가 높았던 Most Popular 과 비교
- 앙상블 모델이 가장 높은 NDCG 점수와 entropy 점수 분포를 보이는 것을 확인

|model| NDCG@15 | entropy@15 |
|---|-------|--------:|
|Ensemble| 0.06151| 3.33082 |  
|base-model-MP| 0.06126| 2.70805 |
|MF| 0.0530| 3.3352 |
|LMF| 0.0542| 3.5511 |