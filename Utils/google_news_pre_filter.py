

##
## This function has two objects
##
##  number 1 is to reduce workload of the DNN sentiment inference, from needing to infer 20 news per stock, 
#   down to only needing to infer 1 stock
##
##  number 2 is to have a more refined set of news source that's more authorative and more representative of the general audience
##
##


import pandas as pd 
import numpy as np

ack_news_source = ['Seeking Alpha', 'Yahoo Finance', 
                    'Industrial IT', 'PRNewswire', 
                    'Business Wire',
                    'Bloomberg', 'Reuters', 'Forbes', 'CNBC', 
                    'Business Insider', 'Fox Business', "CNA"]


def get_empty_raw_news_df():
    one_row = {}
    one_row["title"] = np.nan
    one_row["link"] = np.nan
    one_row["published"] = np.nan
    one_row["source"] = np.nan
    one_row["total_news_today"] = 0
                
    df = pd.DataFrame([one_row])
    return df

def pre_filter_raw_news_df(df):
    df = df[df["source"].isin(ack_news_source)].copy()
    if len(df) == 0:
        return get_empty_raw_news_df()
    else:
        df["total_news_today"] = [len(df)]*len(df)
    return df

