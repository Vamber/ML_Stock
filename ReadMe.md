
<font size="7"> Design Philosophy of ML_stock: </font>

<font size="6"> The big picture: </font>

ML_stock is software which automates the pipeline from 
downloading useful data from internent (currently, google_trend + google_news),
analyzing the downloaded data and select important feature, 
forming various ML_model to binary prediction for stock price tommorow, 
to ultimately employing different expert strategies to decide which portfolio stock to buy tomorrow
(perhaps even use interactive broker to actually them )

This pipline is performed every morning, on hundreds of stocks in Data/stock_and_feature.csv
For example, ML_stock would recommend you to buy (APPL, NVDA, V, TSLA, ... 20 more) before the market opens. 


<font size="6"> 3 design principals: </font>

1. Robust: oftentimes, downloading data from interent may face "turbulance", for example, one day, google trend stops responding. Or the news website you are scraping on may block you for intense request. Therefore, we must give the software the ability to use proxie, detect missing data, redownloading missing data and not block later stage in the pipline in the presence of missing data. 

2. Reflexible: with minimal modification or no modification to the code base, you should be able to, add any new stock and its intended features, add a completely new feature to an existing stock, append a new keyword under a feature to download for a existing stock, while expecting the pipling to immediately take in effects tommorow. Therefore, you should rather think ML_stock as Framework for automation, rather than a static process that keeps making predication in the state of the art. For example, if a really amazing NLP model came out in 2025, we should be able to incorporate it into our ML_stock with almost 0 effort. 

3. Verbose: readiblity is the key to good software. Personally, I think great code flows like English pargraph. Therefore, all the functions inside repo are gonna be really long, such that when you read it, it makes sense of just exactly what it is doing, such as "get_dataset_google_trend_score_for_keyword()". When multilple methods are compose together, it should sound like English. 






Highly Modulized, High flexible implmentation,
with detailed function name as API.

For example, if there is a better neural network for Sentiment Analysis, 
it can be swap into the Program anytime and re-train on the entire dataset

If there is new features that's valuable, it should also be added in there easily

Allows for different ML_models to be trained on the Stock's Feature .
Allows one Model to choose the best subset of features to train on itself.

Allows different stragety to pick the best subset of stock for tomorrow. 





Design Details of ML_Stock 
Data Directory: everything that is Data is stored here (.csv models.bin)
                for example, Features (news sentiment score, google trend score)
                             Logs 
                                  Error (things that failed to download)
                             Feature
                                  Raw_feature
                                  Processed_feature
                                  
                             Models (ML Models that's serializaed, their stats and accuracy, and predition for tomorrow)

                             Expert (evaluates from Model's prediction for tomorrow and decides what stock to buy, and every experts stat)


Coding Details:
1. everything is run from the ML_Stock, therefore consider using absolute Path for everything or relative in which ML_stock is the root
2. the dates, whether as an arguement to a function, or as a column in a data table, must be 2021-03-11  <-- this kind of format 
3. any function failire, such as download error, returns None 


                             
what to do if I want add a new feature
1. create its downloader object and inherit it from downloader template
2. modify generate_stock_features_csv.py to make sure it's included
3. add a new collumn to stock and feature .csv
4. modify downloader_object_hypervisor(), modify 

      