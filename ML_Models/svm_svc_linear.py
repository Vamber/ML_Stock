
from ML_Models.ml_model_template import ml_model_template
import pandas as pd
import numpy as np
from sklearn import svm
from model_generator_template import model_generator_template 

class svm_svc_linear(ml_model_template):


    #important, need to implement this
    model_class_name = "svm_svc_linear"

    #no need to make a new constructor, just inherit from parent

    def __init__(self, suffix) :
        super().__init__("svm_svc_linear", suffix)



    # a very important function which will be used by iterative_5d_sim
    def train_model_and_predict_on_y_test(self, X_train, X_test, y_train, y_test, weight_vec):

        #handling the case when no weight vector is used
        if weight_vec == []:
            weight_vec = None
        
        #runs on training set until accuracy is over 0.6
        term_i = 0
        for i in np.arange(0.1, 2.2, 0.3):
            term_i = i
            clf_linear = svm.SVC(kernel='linear', probability=False, C=i)
            clf_linear.fit(X_train,y_train, sample_weight=weight_vec)
            training_score = clf_linear.score(X_train,y_train)
            if training_score > self.training_termination_accuracy_threshold:
                break

        test_score = clf_linear.score(X_test, y_test)

        y_true = y_test
        y_pred = clf_linear.predict(X_test)
        recall = self.v_recall(y_true, y_pred)

        return [training_score, test_score, recall, term_i]


        
        


 


class svm_svc_linear_generator(model_generator_template):

    def __init__(self):
        super().__init__(svm_svc_linear)






#A = svm_svc_linear_generator()

#A.create_Daily_Prediction()

#K = svm_svc_linear("00000")
#df = K.get_mega_feature_df("ASML")
#df = K.get_truncated_mega_feature_df("ASML")
#print(df)


