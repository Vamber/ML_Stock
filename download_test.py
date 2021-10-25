from Download.google_trend_downloader import google_trend_downloader

A = google_trend_downloader("NVDA", "RTX 3090")
B = google_trend_downloader("NVDA", "buy Nvidia Stock")
C = google_trend_downloader("TSLA", "buy Tesla Stock")

print(C.check_date_for_latest_download())

print(C.f())