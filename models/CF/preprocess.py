from utils import *

class Preprocess():
    def __init__(self,df_book, mediprediction_all_df):
        self.df_book = df_book
        self.mediprediction_all_df = mediprediction_all_df

    def promotion_proprof(self,df):
        from datetime import datetime

        preprocessed_book_df_date = df

        promotion_book_df = preprocessed_book_df_date[preprocessed_book_df_date['date_paid'] >= '2022-01-01']
        promotion_book_df['date_paid_date'] = promotion_book_df['date_paid'].dt.date
        promotion_book_df['date_paid_week'] = promotion_book_df['date_paid_date'].apply(lambda x: x.isocalendar()[1])

        promotion_dict = {
            2:['트리거포인트 침치료'],
            3:['藥徵, 약의 징표','파킨슨병 한의진료','침의 과학적 접근의 이해','길익동동','Medical acupuncture 침의 과학적 접근과 임상활용',\
                '동의보감 약선','수화론(水火論)'],
            4:['실전한약가이드','음양승강으로 해석하는 사상의학: 생리병리'],
            5:['음양승강으로 해석하는 사상의학: 생리병리'],
            6:['윤상훈·권병조의 알짜 근육학','임상 한의사를 위한 기본 한약처방 강의 2판','트리거포인트 침치료','KCD 한방내과 진찰진단 가이드라인',\
                '실전한약가이드','음양승강으로 해석하는 사상의학: 생리병리','藥徵, 약의 징표','증보운곡본초학','통증치료를 위한 근육 초음파와 주사 테크닉'],
            7:['오국통 온병명방'],
            9:['병태생리 Visual map','NEO 인턴 핸드북','보험한약 브런치 the # 2판 개정판','Kendall 자세와 통증치료에 있어서 근육의 기능과 검사 5판',\
                '사상방 사용설명서','실전한약가이드','일차진료 한의사를 위한 보험한약입문 - 둘째 판','증보운곡본초학'],
            10:['한눈에 보는 스트레칭 해부학'],
            11:['임산부에게 사용할 수 있는 한방처방'],
            12:['임산부에게 사용할 수 있는 한방처방'],
            13:['MRI 자신감 키우기_족부편'],
            14:['장골의 PI 변위는 없다'],
            15:['윤상훈·권병조의 알짜 근육학','임상 한의사를 위한 기본 한약처방 강의 2판','KCD 한방내과 진찰진단 가이드라인','트리거포인트 침치료',\
                '음양승강으로 해석하는 사상의학: 생리병리','침의 과학적 접근의 이해','실전한약가이드','임산부에게 사용할 수 있는 한방처방','한눈에 보는 스트레칭 해부학',\
                'MRI 자신감 키우기_족부편'],
            16:['환자상담의 달인','병의원 경영과 자산 관리 클리닉','우리 병원의 문제? 현장에서 답을 찾다!','근육학','스파이랄 및 키네지오 테이핑',\
                '요양병원 주치의 진료핵심'],
            17:['오당 본초강론','운동기능장애 치료 매뉴얼','K. 한의학 임상총론','한방 활용 가이드','최강통증매선','암 치료에 이용되는 천연약물',\
                '왕문원 임상 평형침법','중국 왕문원 평형침구학'],
            18:['초음파 가이드 근골격계 통증 치료의 정석'],
            19:['초음파 가이드 근골격계 통증 치료의 정석','섭혜민 명의경방험안'],
            20:['카이로프랙틱 기본테크닉론'],
            21:['흔히보는 정형외과 외래진료 가이드북'],
            22:['趙紹琴(조소금) 내과학','한의학 상담','숨찬 세상, 호흡기를 편하게',\
                '의학심오(醫學心悟)','안면마비 침구치료','중경서 독법 강해(상,하) /개정판'],
            23:['선생님, 이제 그만 저 좀 포기해 주세요','한의학 상담','숨찬 세상, 호흡기를 편하게',\
            '의학심오(醫學心悟)','중경서 독법 강해(상,하) /개정판','안면마비 침구치료'],
            24:['황황교수의 임상의를 위한 근거기반 상한금궤 처방 매뉴얼','황황교수의 개원 한의사를 위한 상한금궤 처방 강의록',\
            '선생님, 이제 그만 저 좀 포기해 주세요'],\
            25:['황황교수의 임상의를 위한 근거기반 상한금궤 처방 매뉴얼',\
            '황황교수의 개원 한의사를 위한 상한금궤 처방 강의록','약침의 정석 –통증편','갑상선 진료 완전정복',\
            '신경학 증상의 감별법','이것이 알고싶다! 당뇨병진료','어지럼질환의 진단과 치료','증례와 함께 하는 한약처방',\
            '뇌의학의 첫걸음','HAPPY 소아청소년 진료'],\
            26:['약침의 정석 –통증편','갑상선 진료 완전정복','신경학 증상의 감별법',\
            '증례와 함께 하는 한약처방','이것이 알고싶다! 당뇨병진료','HAPPY 소아청소년 진료','어지럼질환의 진단과 치료',\
            '뇌의학의 첫걸음','실전, 임상한의학 내과질환을 중심으로','실전, 임상한의학 알레르기질환','침구대성','평주온열경위'],
            27:['침구과 진료매뉴얼','실전, 임상한의학 내과질환을 중심으로','실전, 임상한의학 알레르기질환','내과학 5권세트','한방순환 신경내과학',\
            '침구대성'],
            28:['감별진단의 정석','기본통증진료학','약처방의 정석 (1, 2권 세트)','QBook: Case based Review',\
                'SMART 내과 1권 : 바이탈, 감염, 종양, 류마티스','일차진료아카데미 처방가이드'],
            29:['비만문답','사암침의 해석과 임상'],
            30:['플로차트 정형외과 진단','침구과 진료매뉴얼','내과학 5권세트','한방순환 신경내과학'],
            31:['외래에서 꼭 알아야 할 통증증후군 137가지'],
            32:['SMART 기본 일차진료매뉴얼 3판(세트)','SMART 소아진료매뉴얼 3판','SMART 응급진료매뉴얼(세트)'],
            33:['SMART 기본 일차진료매뉴얼 3판(세트)','SMART 소아진료매뉴얼 3판','SMART 응급진료매뉴얼(세트)'],
            34:['초음파 유도하 침 시술 가이드북'],
            35:['영어 진료 가이드북','초음파 유도하 침 시술 가이드북'],
            36:['영어 진료 가이드북','소아피부질환해설'],
            37:['소아피부질환해설','醫學心悟(의학심오) 톺아보기'],}

        promotion_item_list = []
        for promotion_items in promotion_dict.values():
            for item in promotion_items:
                promotion_item_list.append(item)

        # set(promotion_item_list), len(set(promotion_item_list))

        preprocess_promotion_df = promotion_book_df[~((promotion_book_df['name_x'].str.contains('침의 과학적 접근과 임상활용')) & \
                                (promotion_book_df['date_paid_week']==3))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('의학심오')) & \
                                    (preprocess_promotion_df['date_paid_week']==22))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('의학심오')) & \
                                    (preprocess_promotion_df['date_paid_week']==23))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('약처방의 정석')) & \
                                    (preprocess_promotion_df['date_paid_week']==28))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('초음파 유도하 침')) & \
                                    (preprocess_promotion_df['date_paid_week']==34))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('초음파 유도하 침')) & \
                                    (preprocess_promotion_df['date_paid_week']==34))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('영어 진료 가이드북')) & \
                                    (preprocess_promotion_df['date_paid_week']==35))]
        preprocess_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('영어 진료 가이드북')) & \
                                    (preprocess_promotion_df['date_paid_week']==36))]
        all_promotion_df = preprocess_promotion_df[~((preprocess_promotion_df['name_x'].str.contains('의학심오')) & \
                                    (preprocess_promotion_df['date_paid_week']==37))]

        for key,value in promotion_dict.items():
            all_promotion_df = all_promotion_df[~((all_promotion_df['name_x'].isin(value)) & (all_promotion_df['date_paid_week']==key))]

        return all_promotion_df




    def train_test_split(self,df_book):
        from datetime import datetime, timedelta
        df_book['date_paid'].max()

        print('train split 날짜:', datetime(2022,9,13)-timedelta(days=21))

        date = '2022-08-23'
        train_before = df_book[df_book['date_paid'] < date]
        train_before_preprocess = self.promotion_proprof(train_before)
        test_before_preprocess = df_book[df_book['date_paid'] >= date]


        #중복 확인 

        # product_ids, name_x 수는 일치
        print('아이템 중복수 확인:',len(df_book.product_ids.unique()), len(df_book.name_x.unique()))

        # 중복 제거 후 수 비교 확인
        print('중복 일치 여부 확인:', len(df_book.drop_duplicates(subset=['product_ids','name_x']).name_x.unique()))

        test = test_before_preprocess
        # train 변수 명 변경
        train = train_before_preprocess

        # test 전처리 진행했을 경우
        print('원본 train 수:', len(train))
        print('원본 test 수:', len(test))

        print('train 유저 수:',len(train.customer_id.unique()),'test 유저 수:',len(test.customer_id.unique()))

        # train test 아이템 중복 확인
        # 신규 유저는 MP 같은 다른 방법으로 추천 진행해야 함
        print('test 만 있는 신규 유저 :',len(set(test['customer_id'].unique())- set(train['customer_id'].unique())))
        print('train 아이템 수 :',len(set(train.product_ids)), 'test 아이템 수 :',len(set(test.product_ids)))
        self.train = train
        self.test = test
        
        return train, test

    def make_sparse_matrix(self, train):
        PdIds = train.product_ids.unique()

        PdIdToIndex = {}
        indexToPdId = {}

        colIdx = 0

        for PdId in PdIds:
            PdIdToIndex[PdId] = colIdx
            indexToPdId[colIdx] = PdId
            colIdx += 1

        userIds = train.customer_id.unique()

        userIdToIndex = {}
        indexToUserId = {}

        rowIdx = 0

        for userId in userIds:
            userIdToIndex[userId] = rowIdx
            indexToUserId[rowIdx] = userId
            rowIdx += 1

        import scipy.sparse as sp

        rows = []
        cols = []
        vals = []

        for row in train.itertuples():
            rows.append(userIdToIndex[row.customer_id])
            cols.append(PdIdToIndex[row.product_ids])
            vals.append(1)

        purchase_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(rowIdx,colIdx))

        matrix = purchase_sparse.todense()

        # Sparsity: 얼마나 비어있나?
        matrix_size = purchase_sparse.shape[0]* purchase_sparse.shape[1]
        num_purchases = len(purchase_sparse.nonzero()[0])
        sparsity = 100 * (1 - (num_purchases / matrix_size))

        print('sparsity 수치:',sparsity)

        self.PdIdToIndex = PdIdToIndex
        self.indexToPdId = indexToPdId
        self.userIdToIndex = userIdToIndex
        self.indexToUserId = indexToUserId
        self.purchase_sparse = purchase_sparse
        self.matrix = matrix
        
        return PdIdToIndex, indexToPdId, userIdToIndex, indexToUserId, purchase_sparse, matrix

    def medisteam_prediction_matrix(self):

        '''    
        - 메디스트림 메디마켓에서 제공하는 정렬 추천 성능 비교를 위한 df 구현
        - 인기도순, 최신순, 과거순, 높은 가격순, 낮은 가격순, 이름순 (총 6 가지)
        - 각각 구현해보고 학습 모델 대비 성능 비교
        '''

        most_popular = self.mediprediction_all_df.groupby(['product_ids']).count()['customer_id'].reset_index()

        medistream_prediction_df = self.mediprediction_all_df[['date_created','regular_price','sale_price','three_months','product_ids','name_x']]
        medistream_prediction_preprop_df = medistream_prediction_df.drop_duplicates(subset=['product_ids'], ignore_index=True)
        medistream_prediction_preprop_df['date_created'] = pd.to_datetime(medistream_prediction_preprop_df['date_created'])
        
        # sale_prices가 0이면 regular_price 값으로 채워넣어야하는데 0이 없음(전처리 필요 무)
        self.most_popular = most_popular
        self.medistream_prediction_preprop_df = medistream_prediction_preprop_df
        return most_popular, medistream_prediction_preprop_df

    def make_ground_trues(self, test):
        # real test 
        ground_trues = []
        for user_id in test['customer_id'].unique():
            ground_trues.append({'id': user_id,\
            'items':list(test[test['customer_id']==user_id].product_ids)
            })

        return ground_trues

    def preprocessing(self):
        train, test = self.train_test_split(self.df_book)
        PdIdToIndex, indexToPdId, userIdToIndex, indexToUserId, purchase_sparse, matrix = ground_tures = self.make_sparse_matrix(train)
        ground_trues = self.make_ground_trues(test)
        most_popular, medistream_prediction_preprop_df = self.medisteam_prediction_matrix()

        return PdIdToIndex, indexToPdId, userIdToIndex, indexToUserId, purchase_sparse, matrix, ground_trues, most_popular, medistream_prediction_preprop_df