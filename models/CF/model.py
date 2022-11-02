import argparse 
from utils import *
from dataload import Dataload
from preprocess import Preprocess
from evaluation import CustomEvaluator

class train():
    def __init__(self,df_book=None,mediprediction_all_df=None,factor=None,regularization=None,iteration=None,top=None):
        self.df_book = df_book
        self.mediprediction_all_df = mediprediction_all_df
        self.factor = factor
        self.regularization = regularization
        self.iteration = iteration
        self.top = top
        


    def train(self):
        df_book = self.df_book
        mediprediction_all_df = self.mediprediction_all_df
        preprocessing = Preprocess(df_book, mediprediction_all_df)
        PdIdToIndex, indexToPdId, userIdToIndex, indexToUserId, \
            purchase_sparse, matrix, ground_trues, most_popular, \
                medistream_prediction_preprop_df = preprocessing.preprocessing()
                
        test = preprocessing.test
        train = preprocessing.train

        # 인기도순
        medistream_popular_list = medistream_prediction_preprop_df.sort_values(by='three_months', ascending=False).index
        # 최신순
        medistream_latest_list = medistream_prediction_preprop_df.sort_values(by='date_created', ascending=False).index
        # 오랜된 순
        medistream_oldest_list = medistream_prediction_preprop_df.sort_values(by='date_created', ascending=True).index
        # 높은 가격 순
        medistream_high_price_list = medistream_prediction_preprop_df.sort_values(by='sale_price', ascending=False).index
        # 낮은 가격 순
        medistream_low_price_list = medistream_prediction_preprop_df.sort_values(by='sale_price', ascending=True).index
        # 이름 순
        medistream_name_sort_list = medistream_prediction_preprop_df.sort_values(by='name_x',ascending=True).index
        
        medipop_lmf_mix_hyper_parameter = {'factor':[],'regularization':[],'iteration':[],'top':[],'NDCG':[],'entropy':[]}

        factor = self.factor
        regularization = self.regularization
        iteration = self.iteration
        top = self.top

        lmf_model = LMF(factors=factor, regularization=regularization, iterations = iteration, random_state=42)
        lmf_model.fit(purchase_sparse, show_progress=False)

        # test 예측값
        lmf_predict_list = []
        for user_id in test['customer_id'].unique():
            try:
                train_purchase_list = list(train[train['customer_id']==user_id].product_ids)
                medi_popular_top_three = medistream_popular_list[:top]
                medi_popular_top_three_list = [medistream_prediction_preprop_df.product_ids.loc[num] for num in medi_popular_top_three \
                                                                    if medistream_prediction_preprop_df.product_ids.loc[num] not in train_purchase_list \
                                                                    ]
                result = lmf_model.recommend(userIdToIndex[user_id], purchase_sparse[userIdToIndex[user_id]], N=20)
                result_list = [indexToPdId[num] for num in result[0]]

                # top 3개 랜덤으로 넣기
                # for medi_popular in medi_popular_top_three_list[:3]:
                #     result_list.insert(np.random.randint(3,7), medi_popular)
                # medi_pop_lmf_list = list(dict.fromkeys(result_list))

                medi_pop_lmf_list = list(dict.fromkeys(medi_popular_top_three_list[:3] + result_list))
                lmf_predict_list.append({'id':user_id ,'items':medi_pop_lmf_list})
            except:
                train_purchase_list = list(train[train['customer_id']==user_id].product_ids)
                lmf_predict_list.append({'id':user_id ,'items':[medistream_prediction_preprop_df.product_ids.loc[num] for num in medistream_popular_list \
                                                                    if medistream_prediction_preprop_df.product_ids.loc[num] not in train_purchase_list \
                                                                    ]})

        # 15 개만 예측하기
        for idx, pred_list in enumerate(lmf_predict_list):
            lmf_predict_list[idx]['items'] = pred_list['items'][:15]
        # LMF
        evaluator = CustomEvaluator()
        ndcg, entropy = evaluator._eval(ground_trues, lmf_predict_list)

        medipop_lmf_mix_hyper_parameter['factor'].append(factor)
        medipop_lmf_mix_hyper_parameter['regularization'].append(regularization)
        medipop_lmf_mix_hyper_parameter['iteration'].append(iteration)
        medipop_lmf_mix_hyper_parameter['top'].append(top)
        medipop_lmf_mix_hyper_parameter['NDCG'].append(ndcg)
        medipop_lmf_mix_hyper_parameter['entropy'].append(entropy)

        print(medipop_lmf_mix_hyper_parameter)
        
        predict_list = pd.DataFrame(lmf_predict_list)
        

        return (pd.DataFrame(medipop_lmf_mix_hyper_parameter), predict_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CF recommendation')
    parser.add_argument('--order_path', default='/fastcampus-data/select_column_version_4.json')
    parser.add_argument('--product_path', default='/fastcampus-data/products/products.json')
    parser.add_argument('--factor', default=40)
    parser.add_argument('--regularization', default=0.005)
    parser.add_argument('--iteration', default=50)
    parser.add_argument('--top', default=20)
    parser.add_argument('--result_download_path', default='/home/user_3/medistream-recsys/models/CF/')
    args = parser.parse_args()

    # 데이터 로드
    dataload = Dataload(order_path=args.order_path,\
                    product_path=args.product_path,\
                    train_month=5)
                    
    df_book,mediprediction_all_df = dataload.dataload()

    # 모델 학습
    model_train = train(df_book,\
        mediprediction_all_df,\
        args.factor, \
        args.regularization,\
        args.iteration,\
            args.top)

    evaluate_df,predict_list = model_train.train()
    # predict_list.to_csv(args.result_download_path+'predict_list.csv')