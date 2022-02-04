

import pandas as pd

import numpy as np


ROOT = "/home/vamber/ML_stock/"

ack_news_source = ['Seeking Alpha', 'Yahoo Finance', 
                    'Industrial IT', 'PRNewswire', 
                    'Business Wire',
                    'Bloomberg', 'Reuters', 'Forbes', 'CNBC', 'Business Insider', 'Fox Business', "CNA"]


def get_row_based_on_NASDAQ(NASDAQ_code):
    df_stocks = pd.read_csv(ROOT + "Data/stock_and_features.csv")
    row = df_stocks[df_stocks["Nasdaq_code"] == NASDAQ_code]
    return row.iloc[0]

def get_news_kw_lst(row_of_stock):
        return str_to_lst(row_of_stock["news_kw_lst"])

def str_to_lst(string):
    return string.strip("[").strip("]").split(",")

def get_all_nasdaq_code():
    ROOT = "/home/vamber/ML_stock/"
    df = pd.read_csv(ROOT + "Data/stock_and_features.csv")
    lst = list(df["Nasdaq_code"])
    return lst

def get_path(Nasdaq_code, kw, date, keep_source=False):
    ROOT = "/home/vamber/ML_stock/"
    df_path = ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Google_News/"+ kw + "/" + date + ".csv"
    return df_path

def get_empty_process_news_df():
    one_row = {}
    one_row["title"] = np.nan
    one_row["source"] = np.nan
    one_row["total_news_today"] = 0
    one_row["sentiment_score"] = 0
                
    df = pd.DataFrame([one_row])

    return df

def filter_processed_news_df(df):
    df = df[df["source"].isin(ack_news_source)].copy()
    if len(df) == 0:
        return get_empty_process_news_df()
    else:
        df["total_news_today"] = [len(df)]*len(df)
    return df

def get_dates_processed_for_a_news_kw(Nasdaq_code, kw):
    ROOT = "/home/vamber/ML_stock/"
    df_path = ROOT + "/Data/Feature/" + Nasdaq_code + "/Raw_Features/Google_News/"+ kw + "/" + "dates_processed" + ".csv"
    df = pd.read_csv(df_path)
    df = df.sort_values(by="dates")
    return list(df["dates"])



for stock in get_all_nasdaq_code():
    stock_row = get_row_based_on_NASDAQ(stock)
    kw_lst = get_news_kw_lst(stock_row)
    for kw in kw_lst:
        dates = get_dates_processed_for_a_news_kw(stock, kw)
        for date in dates:
            path = get_path(stock, kw, date)
            print(stock + " " + kw + " " + date)
            df = pd.read_csv(path)
            df = filter_processed_news_df(df)
            df.to_csv(path, index=False)

