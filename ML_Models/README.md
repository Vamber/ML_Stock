# ML_Models 

### Description:
    ML_Models is the down-stream of Download module. This module is completely encapulated from Download module.
    The only way in which the two modules exchange information is by Data directory. In which Download module writes to the Data directory and ML_models read from there. 

### Ultimate goal:
    The ultimate goal is on each today, produce 5 dfs, 
        1.todays predition, 
        2.historicall accuracy 
        3.historical recall
        4.last_10d_acc
        5.last_10d_recall
    and for course, each df frame is for all stocks, from different ml_model_template and its different suffix


### Sub_Goal:
    The ML_Model impletements the ml_model_template object, it is an interface in which every ml_model (LSTM, SVM, LR, LogR) that is instantiated needs to obey. The interface is an abstraction for:
    0. creating mega_feature_df
    1. feature engineering  
    2. training models
    3. serializing the model trained 
    4. making predictions

### ml_model_gen:
    in every model implementation, for example, svm_svc.py there will be two classes. The first one is the actual model class that inherits from ml_model_tempate which actually implements how to train models and save serialization. The second class is a model_generator, that is responsible for generating a series of model of the same class with different feature engieering, for example, a svm_svc will generate svm_svc_0000, svm_svc_1023, svm_svc_0011, svm_svc_0013. 

### Encoding of model suffix:
    When you see a model by the name of svm_svc_0000()
    : the 3 ending bits has the implication
    bit 0 (dimensionality reduction):
        1. 0 means no dimensionality reduction
        2. 1 means _m6 features has been elimninated
        3. 2 means _m6 + _m5 feature has been eliminated
        4. 3 means _m6, _m5, _m4 features has been eliminated ...
        ....
    bit 1 (normalization) (this function must be called before everything else):
        1. 0 means no normalization
        2. 1 means normalized from _m6 -> _m0
        3. 2 means normalized + each term is computed as the change from prev date (also measning dropping _m6 since _m6 doesn't have a prev_date anymore)

        ....
    bit 2 (feature selection) 
        1. 0 means no feature selection, using all features
        2. 1 means only using sentiment_min
        3. 2 means only using sentiment_max
        4. 3 means only using sentiment_mean
        ....

    bit 3 (drop open and close + compute daily diff)
        1. 0 means do nothing 
        2. 1 means to compute the daily change as a feature close_m0 - open_m0 , close_m1 - open_m1 ... (the change is more meaningful than just open and close)
           and then we also drop the the open and close
    
    bit 4 (training against weights)
        1. 0 means train against no weights
        2. 1 means giving more weight to recent dates
        3. 2 means giving more weight to (big increase or decrease)
        4. 3 means a combination of previous 2 
        ....
    
    Example: lstm_ful_0213 means an lstm model with fully connected layers, that dose no dimensionality reduction, does normalize, using sentiment_min, and does training against weights. 


### iterative 5 day simulation
    So the idea is that since our data is extremely date dependent, just looking at the accuracy of training set vs testing 
    is very misleading. When the software is deployed, what happens is that we train the model every Satuday, and it does prediction for the upcoming week. Therefore we need to simulate this training in this manner. 
    Suppose the dataset is 470 in length, then we need to devide it as 
        1. (0-375) trains on 0-370 predicts 370->375
        2. (0-380) trains on 0-375 predicts 375->380
        3. (0-385) trains on 0-380 predicts 380->385
        4.  ...
        20. (0-470) trains on 0-465 predicts 463->470

        And finally compute the accuracy and recall of this 


