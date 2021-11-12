from Download.google_trend_downloader import google_trend_downloader

from Download.google_news_downloader import google_news_downloader

from Download.stock_price_downloader import stock_price_downloader

#A = google_trend_downloader("NVDA", "buy Nvidia stock")

#print(A.describe())

#B = google_news_downloader("NFLX", "netflix stock")

#B.download_raw_feature_data()

#C = stock_price_downloader("TWD")

#C.download_raw_feature_data()

f = google_trend_downloader.sanity_check_if_keyword_has_data_on_default_start_date()
df = f("MSFT", "2018-2-16", "efjwoif ioefjoew")
print(df)