from typing import Tuple

import pandas as pd

def split_units(value: str) -> Tuple[str, str]:
    column_splited = value.split(' ')
    unit = ' '.join(column_splited[1:])
    try:
        quantity = float(column_splited[0])
    except ValueError:
        try:
            num, denom = column_splited[0].split('/')
            quantity = float(num)/float(denom)
        except ValueError:
            quantity = 1
            unit = value

    return quantity, unit

def normalize_by_qtd(row: pd.Series) -> pd.Series:
    qtd = row.qtd
    row[3:] = row[3:]/qtd
    row.qtd = 1

    return row

def apply_preprocess(df: pd.DataFrame, inflation: float = 20.4397) -> pd.DataFrame:
    df_processed = df.copy()
    df_processed[['qtd', 'unit']] = df.apply(lambda row: split_units(row.unit), axis=1, result_type='expand')
    df_processed = df_processed.apply(lambda row: normalize_by_qtd(row), axis=1)
    df_processed = df_processed.drop('qtd', axis=1)
    
    df_processed['price_cents'] = df_processed.price_cents.map(lambda price: price*(1 + inflation)/100)
    df_processed = df_processed.rename(columns={'price_cents': 'USD'})

    return df_processed