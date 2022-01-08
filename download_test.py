
from Download.feature_downloader_hypervisor import create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv
from Download.google_trend_downloader import google_trend_downloader
from Download.google_news_downloader import google_news_downloader

import pandas as pd

A = google_trend_downloader("NVS", "pfizer stock", "2021-10-10")
A.download_raw_feature_data()

#print(A.describe())

#B = google_news_downloader("BABA", "alibaba stock", "2021-10-10")

#B.download_raw_feature_data()

print(B.describe())

#C = stock_price_downloader("TWD")

#C.download_raw_feature_data()



1/0

df = pd.read_csv("Data/stock_and_features.csv")




one_row =df.iloc[-1]

print(one_row)

H = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(one_row)

H.describe()