import pandas as pd
import matplotlib.pyplot as plt

def lag_day(df, colname = 'total_volume', lag = 1):

    keys = ['InvoiceDate_only', 'cluster']

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
    
    cl = g.name # this part is for df..groupby(['StockCode','Country','cluster'], group_keys=False).apply()

    g = g.set_index('InvoiceDate_only').asfreq('D')

    g = g.assign(cluster=cl)

    g['total_volume'] = g['total_volume'].fillna(0)
    g['total_sales_price'] = g['total_sales_price'].fillna(0)

    idx = g.index
    g['Year'] = idx.year
    g['Month'] = idx.month
    g['Week'] = idx.isocalendar().week.astype(int)
    g['WeekdayNum'] = idx.weekday

    return g.reset_index().rename(columns={'index':'InvoiceDate_only'})


def plot_history(res, metric = 'rmse'):
    epochs = len(res['validation_0'][metric])
    x_axis = range(0, epochs)

    plt.figure(figsize=(10, 6))
    plt.plot(x_axis, res['validation_0'][metric], label=f'Train {metric}')
    plt.plot(x_axis, res['validation_1'][metric], label=f'Validation {metric}')
    plt.xlabel("Boosting Round")
    plt.ylabel(f"{metric}")
    plt.title(f"Training vs Validation {metric}")
    plt.legend()
    plt.show()


def predict_plot(model, feature_set, full_data, y, X):
    y_pred = model.predict(feature_set)

    pred_df = pd.DataFrame({
        "InvoiceDate_only": full_data[X].values,
        "y_actual": full_data[y].values,
        "y_pred": y_pred
    })

    daily = pred_df.groupby("InvoiceDate_only")[["y_actual", "y_pred"]].sum().reset_index()

    plt.figure(figsize=(12, 6))
    plt.plot(daily["InvoiceDate_only"], daily["y_actual"], label="Actual", linewidth=2)
    plt.plot(daily["InvoiceDate_only"], daily["y_pred"], label="Predicted", linewidth=2, linestyle="--")
    plt.xlabel("Date")
    plt.ylabel("Total Quantity Sold")
    plt.title("Actual vs Predicted Daily Quantity")
    plt.legend()
    plt.tight_layout()
    plt.show()