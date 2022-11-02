# Demo Web application
## 목적
프로젝트를 통해 만든 모델이 어떻게 사용자에게 추천이 되는지 프로토 타입페이지를 통해 확인이 가능합니다.

## 설명
### 1. index.html
사용자가 로그인 이후, 추천페이지를 열었을 때 추천받는 책들 목록입니다.  
CF 모델을 사용하여, 사용자가 이전에 구입했던 책과 가장 인기있는 책을 기준으로 개인화된 추천을 받게 됩니다.
<img width="1850" alt="image" src="https://user-images.githubusercontent.com/68417368/199475212-59eed04f-fcc9-4a70-9005-400143332bbc.png">

### 2. photo-detail.html
사용자가 책을 클릭했을 때 보이는 상세 페이지입니다.  
CBF 모델을 사용하여, 해당 책과 가장 가까운 책 15권을 추천받습니다.
<img width="1815" alt="image" src="https://user-images.githubusercontent.com/68417368/199475499-84378d37-45bd-4330-9cc0-aa306b1dd1e0.png">

## 실행방법
<code> FLASK_APP=demo flask run </code>
