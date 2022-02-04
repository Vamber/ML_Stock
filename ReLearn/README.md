# ReLearn

## Goal
The issue which ReLearn wants to solve is the following: sometimes the keyword we pick (google trend ) are just not very correlated with the stock price, for example if we pick etheruem and Nvidia, we might think those two are very correlated, but actually they are not that correlated), this bad choice of kw could cause our model perform poorly in hist_acc or hist_recall. Therefore, we need a sysmtic and automatic for the software to choose new kw on its own. For example, finding bitcoin and nvidia is more correlated. 

## Implementation
Every satuday, the software would take 2 stocks with the lowest hist_acc and 2 stock with highest recall (let's call them A, B, C, D). 
The software remove them with the "generate_stock_features_csv.py" module. 
And then it will save the news_kw (because it will be too costly to redo all the sentiment analysis with neural nets). 
It saves the news kw. It also saves all existing trend kw. 
(with the help of good_trend_kw_filter), it automatically searches for new kw, and inserts it back in. 

