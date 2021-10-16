

import yfinance as yf

msft = yf.Ticker("TSLA")
hist = msft.history(period ="max")
print(hist)
