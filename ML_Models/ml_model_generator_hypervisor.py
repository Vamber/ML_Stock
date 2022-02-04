

###
### This is the module that finally glues everything together
###
### It is responsible for holding n ml_model generate (<- which hold k model of different suffix),
###
### And this will produce the 5dfs as the final output handed into the downwards module

from ML_Models.svm_svc_linear import svm_svc_linear_generator
from ML_Models.svm_svc_rbf import svm_svc_rbf_generator
import os
from os import path
from datetime import date
from functools import reduce
import pandas as pd

class ml_model_generator_hypervisor():

    def __init__(self, ml_model_generator_lst):
        self.ml_model_generator_lst = [mmg() for mmg in ml_model_generator_lst]
        self.ROOT = "/home/vamber/ML_stock"
        self.daily_prediction_dir = self.ROOT + "/Data/ML_Models/Daily_Prediction/"
        if not path.exists(self.daily_prediction_dir):
            os.makedirs(self.daily_prediction_dir)


    ##
    ##
    def train_and_save_all_ml_model_generator(self):
        for ml_model_generator in self.ml_model_generator_lst:
            ml_model_generator.train_and_save_all_ml_models()


    ##
    ##
    def run_iterative_5d_sim_on_all_stocks(self):
        for ml_model_generator in self.ml_model_generator_lst:
            ml_model_generator.run_iterative_5d_sim_on_all_stocks()


    ##
    ## forgive for the horrible way I coded this function
    def create_daily_prediction(self):

        #note, use mmg to short for ml_model_generator
        mmg_daily_prediction_df_lst = []
        mmg_hist_acc_df_lst = []
        mmg_hist_recall_df_lst = []
        mmg_last_10d_acc_df_lst = []
        mmg_last_10d_recall_df_lst = []
        #
        today = str(date.today())
        today_hypervisor_predition_dir = self.daily_prediction_dir + today
        if not path.exists(today_hypervisor_predition_dir):
            os.makedirs(today_hypervisor_predition_dir)

        for mmg in self.ml_model_generator_lst:

            ##
            ##
            mmg.create_mmg_daily_prediction()

            mmg_today_dir = mmg.daily_prediction_dir + "/" + today + "/"
            #
            mmg_daily_prediction_df = pd.read_csv(mmg_today_dir + "prediction.csv")
            mmg_daily_prediction_df_lst.append(mmg_daily_prediction_df)
            #
            mmg_hist_acc_df = pd.read_csv(mmg_today_dir + "hist_acc_df.csv")
            mmg_hist_acc_df_lst.append(mmg_hist_acc_df)
            #
            mmg_hist_recall_df = pd.read_csv(mmg_today_dir + "hist_recall_df.csv")
            mmg_hist_recall_df_lst.append(mmg_hist_recall_df)
            #
            mmg_last_10d_acc_df = pd.read_csv(mmg_today_dir + "last_10d_acc_df.csv")
            mmg_last_10d_acc_df_lst.append(mmg_last_10d_acc_df)
            #
            mmg_last_10d_recall_df = pd.read_csv(mmg_today_dir + "last_10d_recall_df.csv")
            mmg_last_10d_recall_df_lst.append(mmg_last_10d_recall_df)

        lst_of_mmg_df_lst = [mmg_daily_prediction_df_lst, mmg_hist_acc_df_lst, mmg_hist_recall_df_lst, mmg_last_10d_acc_df_lst, mmg_last_10d_recall_df_lst]
        lst_of_5_df_name = ["prediction.csv", "hist_acc_df.csv", "hist_recall_df.csv", "last_10d_acc_df.csv", "last_10d_recall_df.csv"]

        for i in range(0,5):
            df_i = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), lst_of_mmg_df_lst[i])
            df_i = df_i.drop(columns=[c for c in df_i.columns if "Unnamed" in c])
            df_i_name = lst_of_5_df_name[i]
            df_i.to_csv(today_hypervisor_predition_dir + "/" + df_i_name)

        print("DONE")


#H = ml_model_generator_hypervisor([svm_svc_rbf_generator])
#H.create_daily_prediction()





        





