import pandas as pd

def apply_diet_qtds(row: pd.Series, qtds: list) -> pd.Series:
    """A function to update the cost and unit string of each commodity
    base on a quantities vector.

    Parameters
    ----------
    row : pd.Series
        A row of the dataframe with food, nutrients, and prices.
    qtds : list
        The daily quantities of each food in the diet.

    Returns
    -------
    pd.Series
        A row with the diet commodities, their quantities, and prices.
    """
    qtd = qtds[row.name]*7
    row.unit = f"{qtd:.4f} {row.unit}"
    row.USD = round(qtd*row.USD, 2)
    return row

def compute_weekly_diet_df(df: pd.DataFrame, qtds: list) -> pd.DataFrame:
    """A method that computes the diet from the quantities vector returned
    from the optimization process.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe with food, nutrients, and prices.
    qtds : list
        The daily quantities of each food in the diet.

    Returns
    -------
    pd.DataFrame
        A dataframe with the diet commodities, their quantities, and 
        prices.
    """
    df_diet = df[['commodity', 'unit', 'USD']].reset_index(drop=True).copy()
    df_diet = df_diet.apply(lambda row: apply_diet_qtds(row, qtds), axis=1)
    df_diet = df_diet.sort_values(by='USD', ascending=False).reset_index(drop=True)
    df_diet = df_diet[df_diet.USD != 0]
    df_diet = df_diet.rename(columns={'unit': 'qtd_weekly', 'USD': 'usd_weekly'})

    total_row = pd.Series({
        'commodity': '', 
        'qtd_weekly': 'TOTAL', 
        'usd_weekly': df_diet.usd_weekly.sum(),
    })
    df_diet = pd.concat([df_diet, total_row.to_frame().T], ignore_index=True)

    return df_diet
