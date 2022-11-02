import pandas as pd
import numpy as np
from tqdm import tqdm

import scipy.sparse as sparse
import random
import implicit
from implicit.als import AlternatingLeastSquares as ALS
from implicit.lmf import LogisticMatrixFactorization as LMF




# drop columns 전처리
def drop_columns(delete_columns:list,df:pd.DataFrame) -> pd.DataFrame:
    # 회의 때 얘기한 컬럼 전처리
    # None or 필요 없는 컬럼
    df = df.drop(columns=delete_columns)
    return df

def dict_to_column(columns:list,df:pd.DataFrame) -> pd.DataFrame:
    for col in columns:
        key_set = dict_to_set(col,df)
        df = set_to_column(col,key_set,df)
    return df

def dict_to_set(column:str,df:pd.DataFrame) -> set:
    key_set = set()
    for i in tqdm(df[column]):
        
        # column 내용이 dict일 경우
        if isinstance(i, dict):
            key_set |= set(i.keys())
        
        # column 내용이 None type 일 경우
        elif i == None:
            continue
        
        # column 내용이 [dict]로 감싸져있는 경우
        elif isinstance(i, list)&len(i)>0:
            if isinstance(i[0], str):
                continue
            key_set |= set(i[0].keys())
        


    return key_set

def set_to_column(column:str,key_set:set,df:pd.DataFrame) -> pd.DataFrame:
    for key in key_set:
        
        #중복인 경우 컬럼_중복컬럼으로 추가
        if key in df.columns:
            df[column+'_'+key] = df[column].apply(lambda x: x.get(key, None) if isinstance(x, dict) else None if x==None
                                       else ( None \
                                       if len(x)==0 else ( x[0].get(key, None) \
                                       if isinstance(x[0],dict)  else \
                                           None)) \
                                      )
        #중복이 아닌 경우
        else:
            df[key] = df[column].apply(lambda x: x.get(key, None) if isinstance(x, dict) else None if x==None
                                       else ( None \
                                       if len(x)==0 else ( x[0].get(key, None) \
                                       if isinstance(x[0],dict)  else \
                                           None)) \
                                      )

    df = df.drop(columns=[column])
    return df

# 컬럼안 key 값이 한 개일 경우 딕셔너리만 풉니다!
def key_to_element(element_columns:list,df:pd.DataFrame)->pd.DataFrame:
    for col in element_columns:
        key_set = dict_to_set(col, df)
        assert len(key_set)==1, f'{col}: key가 2개 이상이므로 dict_to_column 함수 이용하세요'
        for key in key_set:
            df[col] = df[col].apply(lambda x: x.get(key,None) if isinstance(x,dict) else None)
    return df

'''
사용 예 log_data_sampling.json

%cd ..
from preprocessing import drop_columns,dict_to_column,dict_to_set,set_to_column

columns = ['_metadata','context','traits','properties']
df = dict_to_column(columns, df)

delete_columns = ['properties_properties', 'properties_version','properties_type', \
                  'properties_category','properties_name']
df = drop_columns(delete_columns, df)

'''