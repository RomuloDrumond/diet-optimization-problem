from typing import Tuple

import pandas as pd

def split_units(unit_str: str) -> Tuple[float, str]:
    """Function to split the string with quantity and unit in two 
    columns.

    Parameters
    ----------
    unit_str : str
        The string with, possibly, a quantity and a unit.

    Returns
    -------
    Tuple[float, str]
        Tuple with (quantity, new_unit_string).
    """
    column_splited = unit_str.split(' ')
    new_unit_str = ' '.join(column_splited[1:])
    try:
        quantity = float(column_splited[0])
    except ValueError:
        try:
            num, denom = column_splited[0].split('/')
            quantity = float(num)/float(denom)
        except ValueError:
            quantity = 1.0
            new_unit_str = unit_str

    return quantity, new_unit_str


def normalize_by_qtd(row: pd.Series) -> pd.Series:
    """Scale nutrient values to one portion of the unit.

    Parameters
    ----------
    row : pd.Series
        The Pandas dataframe row.

    Returns
    -------
    pd.Series
        The Pandas dataframe with nutrients scaled.
    """
    qtd = row.qtd
    row[3:] = row[3:]/qtd
    row.qtd = 1

    return row


def apply_preprocess(df: pd.DataFrame, inflation: float = 20.4397) -> pd.DataFrame:
    """Function to apply all preprocessing steps.

    This function does:
    1. Split units string between quantity and "true" unit;
    2. Normalize nutrients and price for one value of unit;
    2. Apply cumulative inflation to all food prices.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with foods, nutrients, and prices.
    inflation : float, optional
        The cumulative inflation value, by default 20.4397

    Returns
    -------
    pd.DataFrame
        A preprocessed copy of the original dataframe.
    """
    df_processed = df.copy()
    df_processed[['qtd', 'unit']] = df.apply(lambda row: split_units(row.unit), axis=1, result_type='expand')
    df_processed = df_processed.apply(normalize_by_qtd, axis=1)
    df_processed = df_processed.drop('qtd', axis=1)
    
    df_processed['price_cents'] = df_processed.price_cents.map(lambda price: price*(1 + inflation)/100)
    df_processed = df_processed.rename(columns={'price_cents': 'USD'})

    return df_processed
