
from ML_Models.ml_model_template import ml_model_template
import pandas as pd
import numpy as np
from sklearn import svm
from model_generator_template import model_generator_template 




class svm_svc_rbf(ml_model_template):


    #important, need to implement this
    model_class_name = "svm_svc_rbf"

    #no need to make a new constructor, just inherit from parent

    def __init__(self, suffix) :
        super().__init__("svm_svc_rbf", suffix)



    def train_model_util(self, X_train, X_test, y_train, y_test, weight_vec):
         #handling the case when no weight vector is used
        if weight_vec == []:
            weight_vec = None
        
        #runs on training set until accuracy is over 0.6
        term_i = 0
        for i in np.arange(0.1, 2.2, 0.3):
            term_i = i
            clf_rbf = svm.SVC(kernel='rbf', probability=False, C=i)
            clf_rbf.fit(X_train,y_train, sample_weight=weight_vec)
            training_score = clf_rbf.score(X_train,y_train)
            if training_score > self.training_termination_accuracy_threshold:
                break
        
        if y_test is None or X_test is None:
            test_score = -1
            recall = -1

        else:  
            test_score = clf_rbf.score(X_test, y_test)
            y_true = y_test
            y_pred = clf_rbf.predict(X_test)
            recall = self.v_recall(y_true, y_pred)

        return [ clf_rbf, [training_score, test_score, recall, term_i]]




    





 


class svm_svc_rbf_generator(model_generator_template):

    def __init__(self):
        super().__init__(svm_svc_rbf)









#A = svm_svc_rbf_generator()

#A.train_and_save_all_ml_models()

#A.create_Daily_Prediction()


#A.create_Daily_Prediction()

#K = svm_svc_rbf("00000")
#df = K.get_mega_feature_df("AMD", False)
#df.to_csv("test.csv")
#print(df)
#print(list(df.iloc[-1]))

#r = K.predict_stock("REIT")
#print(r)

#K.create_df_of_daily_prediction_for_all_stocks_under_this_suffix()
#K.train_model_and_save("REIT")
#K.predict_stock("REIT")

#print(df.columns)
#print(df.iloc[-1])
#df = K.get_truncated_mega_feature_df("ASML")
#print(df)


