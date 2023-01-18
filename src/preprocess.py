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
