import pandas as pd

def lag_quantity(df, lag = 1):

    keys = ['StockCode','Country','InvoiceDate_only']

    lag_tbl = df[keys + ['total_volume']].copy()
    lag_tbl['InvoiceDate_only'] = lag_tbl['InvoiceDate_only'] + pd.Timedelta(days=lag) 
    lag_col = f'lag_{lag}'
    lag_tbl = lag_tbl.rename(columns={'total_volume': lag_col})

    df = df.merge(lag_tbl, on=keys, how='left')

    df[lag_col] = df[lag_col].fillna(0)

    return df