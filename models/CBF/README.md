# CBF(Contents Based Filtering)
cbf_module.py
## 파일 설명
### 작동 방식
1. raw data에서 input 값과 같은 타이틀의 index를 찾는다.
2. title에 넣은 아이템의 각 topic들에 대한 확률값을 불러온다.
3. 이 확률값을 가지고 코사인 유사도가 가장 높은 순으로 15개의 아이템을 불러오게 된다.
### Run
<code>python cbf_module.py --title --book --article</code>
### Return
list: 입력받은 아이템과 코사인 유사도가 높은 아이템 순으로 [product_number, title, cosine_similarity]의 리스트 반환
### Argument
- title : str, 책 혹은 아티클의 제목을 넣는다.
- book : bool, default=True 책을 검색 대상에 넣을 경우 True.
- article : bool, default=True 아티클을 검색 대상에 넣을 경우 True.
