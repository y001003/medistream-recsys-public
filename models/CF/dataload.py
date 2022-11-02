from utils import *

class Dataload():
    def __init__(self, order_path=None, product_path=None, train_month=None):
        self.order_path = order_path
        self.product_path = product_path
        self.train_month = train_month

    def load(self):
        order_path = self.order_path
        product_path=self.product_path
        train_month=self.train_month
        
        # products name 확인 용
        products_df = pd.read_json(product_path)
        products_df = key_to_element(['_id'],products_df)
        order_df = pd.read_json(order_path)

        from dateutil.relativedelta import relativedelta
        from datetime import datetime

        order_df['date_paid'] = pd.to_datetime(order_df['date_paid'])
        # 5개월 전 날짜 확인
        print(order_df['date_paid'].max()-relativedelta(months=train_month))

        return products_df, order_df

    def product_name_fill(self,order_df:pd.DataFrame())->pd.DataFrame():
        # 각 마지막 product_ids, name으로 채우기
        product_ids_to_name = {}
        for idx, row in order_df.iterrows():
            product_ids_to_name[row.product_ids] = row.name_x
        order_df['name_x'] = order_df['product_ids'].apply(lambda x: product_ids_to_name[x])

        name_to_product_ids = {}
        for idx, row in order_df.iterrows():
            name_to_product_ids[row.name_x] = row.product_ids
        order_df['product_ids'] = order_df['name_x'].apply(lambda x: name_to_product_ids[x])
        return order_df

    def make_input(self,product_name_preprocess_df:pd.DataFrame())->pd.DataFrame():
        # medirecommend 만들기
        product_name_preprocess_df = product_name_preprocess_df.dropna(subset=['product_ids','name_x'])

        # 나오는 개월 수 적기
        date_state = "2022-04-13"
        # paid orders만 가져오기
        product_name_preprocess_df['date_paid'] = pd.to_datetime(product_name_preprocess_df['date_paid'])
        df_only_paid = product_name_preprocess_df[~product_name_preprocess_df['date_paid'].isna()]
        # 취소 안된 것만 가져오기
        complete_df = df_only_paid[(df_only_paid['paid'] == True) & (df_only_paid['cancelled']==False)]
        # 도서 카테고리만 가져오기
        only_book = complete_df[complete_df['name'] == '도서']

        # 유저가 중복으로 아이템 구매 삭제
        df_duplicated_book = only_book.drop_duplicates(subset=['customer_id','product_ids'])

        df_sort = df_duplicated_book.sort_values(by='date_paid').reset_index(drop=True)
        df_sort = self.product_name_fill(df_sort)
        df_sort = df_sort.drop_duplicates(subset=['customer_id','product_ids']).reset_index(drop=True)

        # 5개월치 데이터만 가져오기
        df_book = df_sort[df_sort['date_paid'] >= date_state].reset_index(drop=True)

        # 마지막 3주 제외한 medirecommend 만들기
        mediprediction_all_df = df_sort[df_sort['date_paid'] < '2022-08-23'].reset_index(drop=True)

        return df_book, mediprediction_all_df
    
    def dataload(self):
        product_df, df = self.load()
        product_name_preprocess_df = self.product_name_fill(df)
        df_book, mediprediction_all_df = self.make_input(product_name_preprocess_df)
        
        print('중복 제거 전:',len(product_name_preprocess_df), '중복 제거 후:',len(df_book))
        print('전체 데이터 수:',len(df_book))
        print('아이템 수:',len(df_book.product_ids.unique()),'유저 수:',len(df_book.customer_id.unique()))
        
        return df_book, mediprediction_all_df