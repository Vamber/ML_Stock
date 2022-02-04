

from Utils.google_trends_utils import get_dataset_google_trend_score_for_keyword_in_last_3m

from Utils.stock_dataset_utils import get_dataset_for_a_stock_for_last_year

import pandas as pd

import numpy as np

import sys

def find_corr_between_stock_price_and_trend_kw(Nasdaq_code, trend_kw, enable_print=False):

    df_stock = get_dataset_for_a_stock_for_last_year(Nasdaq_code)
    df_stock = df_stock.reset_index()
    df_stock = df_stock[["Date", "Close"]]
    
    df_stock = df_stock.rename(columns={"Date":"date", "Close":"close"})

    trend_stock = get_dataset_google_trend_score_for_keyword_in_last_3m(trend_kw)
    trend_stock = trend_stock.reset_index()
    trend_stock = trend_stock[["date"] + [trend_kw]]

    two_df = pd.merge(df_stock, trend_stock, on="date", how="inner")


    two_df = two_df[["close", trend_kw]]
    two_df = (two_df - two_df.mean())/two_df.std()


    
    array_close = two_df["close"].to_numpy()
    array_kw = two_df[trend_kw].to_numpy()
    n = array_close.size


    r = lambda x : round(x, 2)

    if enable_print:
        print(" ")
        print(Nasdaq_code)
        print("vs")
        print(trend_kw)
        [print(" ") for i in range(0,2)]

    #pure correlation
    enable_print and print("pure correlation matrix")
    r0 = r( np.corrcoef(array_close, array_kw)[0][1])
    enable_print and print(r0)

    #the correlation for detla between each day 
    enable_print and print("correlation matrix terms by looking at daily delta")
    x = array_close[1:n] - array_close[0:n-1]
    y = array_kw[1:n] - array_kw[0:n-1]
    r1 = r( np.corrcoef(x,y)[0][1]) 
    enable_print and print(r1)

    #find the how today delta in trend impacts tomorrow's stock price
    enable_print and print("correlation by after shifting trend_kw to one day before")
    x = array_close[1:n] - array_close[0:n-1]
    y = array_kw[1:n] - array_kw[0:n-1]
    x = x[1:]
    y = y[0:-1]
    r2 = r (np.corrcoef(x,y)[0][1]) 
    enable_print and print(r2)

    enable_print and [print(" ") for i in range(0,2)]

    return [r0, r1, r0]


def main():
    cmd_args = list(sys.argv)
    stock = cmd_args[1]
    trend = cmd_args[2]
    find_corr_between_stock_price_and_trend_kw(stock, trend, enable_print=True)


if __name__ == "__main__":
    main()





