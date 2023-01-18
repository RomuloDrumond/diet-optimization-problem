import pandas as pd

def apply_diet_qtds(row, qtds):
    qtd = qtds[row.name]*7
    row.unit = f"{qtd:.4f} {row.unit}"
    row.USD = round(qtd*row.USD, 2)
    return row

# TODO: Add total cost to last line
def compute_diet_df(df: pd.DataFrame, qtds: list) -> pd.DataFrame:
    df_diet = df[['commodity', 'unit', 'USD']].reset_index(drop=True).copy()
    df_diet = df_diet.apply(lambda row: apply_diet_qtds(row, qtds), axis=1)
    df_diet = df_diet.sort_values(by='USD', ascending=False).reset_index(drop=True)
    df_diet = df_diet[df_diet.USD != 0]
    df_diet = df_diet.rename(columns={'unit': 'qtd_weekly', 'USD': 'usd_weekly'})
    return df_diet