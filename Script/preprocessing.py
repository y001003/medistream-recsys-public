import pandas as pd
import numpy as np
from tqdm import tqdm

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
        if isinstance(i, dict):
            key_set |= set(i.keys())
        elif isinstance(i, list):
            key_set |= set(i[0].keys())
    return key_set

def set_to_column(column:str,key_set:set,df:pd.DataFrame) -> pd.DataFrame:
    for key in key_set:
        
        #중복인 경우 컬럼_중복컬럼으로 추가
        if key in df.columns:
            df[column+'_'+key] = df[column].apply(lambda x: x.get(key, None) if isinstance(x, dict) else None if x==None
                                       else (x[0].get(key, None) \
                                       if isinstance(x[0],dict) else None) \
                                      )
        #중복이 아닌 경우
        else:
            df[key] = df[column].apply(lambda x: x.get(key, None) if isinstance(x, dict) else None if x==None
                                       else (x[0].get(key, None) \
                                       if isinstance(x[0],dict) else None) \
                                      )

    df = df.drop(columns=[column])
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