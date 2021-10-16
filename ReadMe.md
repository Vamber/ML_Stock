
Design Philosophy of ML_stock:

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
                             Models (ML Models that's serializaed, their stats and accuracy, and predition for tomorrow)

                             Expert (evaluates from Model's prediction for tomorrow and decides what stock to buy, and every experts stat)


Coding Details:
1. everything is run from the ML_Stock, therefore consider using absolute Path for everything
2. the dates, whether as an arguement to a function, or as a column in a data table, must be 2021-03-11  <-- this kind of format 
3. any function failire, such as download error, returns None 


                             

      