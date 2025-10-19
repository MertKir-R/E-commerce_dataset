import pandas as pd

def lag_day(df, colname = 'total_volume', lag = 1):

    keys = ['StockCode','Country','InvoiceDate_only']

    lag_tbl = df[keys + [colname]].copy()
    lag_tbl['InvoiceDate_only'] = lag_tbl['InvoiceDate_only'] + pd.Timedelta(days=lag) 
    lag_col = f'lag_{colname}_{lag}'
    lag_tbl = lag_tbl.rename(columns={colname: lag_col})

    df = df.merge(lag_tbl, on=keys, how='left')

    df[lag_col] = df[lag_col].fillna(0)

    return df



def lag_avg(df, colname = 'total_volume', lag = 7):
    # shift(1) removes today, rolling(7) averages the previous 7 rows
    lag_col = f'avg_{colname}_{lag}'
    df[lag_col]  = df[colname].shift(1).rolling(lag, min_periods=1).mean()
    return df


def calendar_fillzero(g):
    
    sc, country, cl = g.name # this part is for df..groupby(['StockCode','Country','cluster'], group_keys=False).apply()

    g = g.set_index('InvoiceDate_only').asfreq('D')

    g = g.assign(StockCode=sc, Country=country, cluster=cl)

    g['total_volume'] = g['total_volume'].fillna(0)
    g['total_sales_price'] = g['total_sales_price'].fillna(0)

    idx = g.index
    g['Year'] = idx.year
    g['Month'] = idx.month
    g['Week'] = idx.isocalendar().week.astype(int)
    g['WeekdayNum'] = idx.weekday

    return g.reset_index().rename(columns={'index':'InvoiceDate_only'})