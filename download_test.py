
from Download.feature_downloader_hypervisor import create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv

import pandas as pd

#A = google_trend_downloader("NVDA", "buy Nvidia stock")

#print(A.describe())

#B = google_news_downloader("NFLX", "netflix stock")

#B.download_raw_feature_data()

#C = stock_price_downloader("TWD")

#C.download_raw_feature_data()


df = pd.read_csv("Data/stock_and_features.csv")




one_row =df.iloc[-1]

print(one_row)

H = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(one_row)

H.describe()