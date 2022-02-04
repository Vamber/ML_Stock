

import pandas as pd
from known_suffix_lst import known_suffix_lst
import concurrent.futures
from os import path
import os
from datetime import date
from functools import reduce


##
## A model generator template which every ML_model needs to follow 
##

class model_generator_template():

    def __init__(self, ml_model_type):
        self.model_type = ml_model_type
        self.suffix_lst = known_suffix_lst
        self.ml_model_lst = []
        self.ROOT = "/home/vamber/ML_stock/"
        for suffix in self.suffix_lst:
            self.ml_model_lst.append(self.model_type(suffix))

        self.daily_prediction_dir = self.ROOT + "/Data/ML_Models/" + ml_model_type.model_class_name + "/Daily_Prediction/"
        if not path.exists(self.daily_prediction_dir):
            os.makedirs(self.daily_prediction_dir)



    #A helpful function used by run_iterative_4d_sim_on_all_stocks
    def make_proc(self, ml_model, Nasdaq_code):
        return lambda : ml_model.run_iterative_5d_sim_on_stock_dataset(Nasdaq_code)

    #helper function
    def get_nasdaq_code_lst(self):
        df_path = self.ROOT + "/Data/stock_and_features.csv"
        df = pd.read_csv(df_path)
        nasdaq_lst = list(df["Nasdaq_code"])
        return nasdaq_lst


    #CORE
    def run_iterative_5d_sim_on_all_stocks(self):
       
        nasdaq_lst = self.get_nasdaq_code_lst()

        lst_of_sim_process = []
        #now the simulation begins
        for nasdaq in nasdaq_lst:
            for ml_model in self.ml_model_lst:
                p = self.make_proc(ml_model, nasdaq)
                lst_of_sim_process.append(p)
      
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            print("There are " + str(len(lst_of_sim_process)) +  " process needed to be run")
            [executor.submit(proc) for proc in lst_of_sim_process]

        #finish
        print("DONE !")

    
    #CORE
    def train_and_save_all_ml_models(self):
        nasdaq_lst = self.get_nasdaq_code_lst()

        for nasdaq in nasdaq_lst:
            for ml_model in self.ml_model_lst:
                ml_model.train_model_and_save(nasdaq)



    #Core 
    def create_mmg_daily_prediction(self):
        today_daily_prediction_work_dir = self.daily_prediction_dir + "/" + str(date.today()) + "/"
        if not path.exists(today_daily_prediction_work_dir):
            os.makedirs(today_daily_prediction_work_dir)

        #this is suppose to be 2D list, and an item is a dataframe
        hist_acc_df_lst = []
        hist_recall_df_lst = []
        last_10d_acc_df_lst = []
        last_10d_recall_df_lst = []
        stock_prediction_df_lst = []

        #each ml_model is basically the same model but with a different suffix
        #such as ml_model 00000, ml_model40000 ... sorry for the confusion

        for ml_model_of_suffix in self.ml_model_lst:
            #
            acc_recall_4dfs_lst = ml_model_of_suffix.create_4dfs_of_acc_and_recall_for_all_stocks_under_this_suffix()
            hist_acc_df_lst.append(acc_recall_4dfs_lst[0])
            hist_recall_df_lst.append(acc_recall_4dfs_lst[1])
            last_10d_acc_df_lst.append(acc_recall_4dfs_lst[2])
            last_10d_recall_df_lst.append(acc_recall_4dfs_lst[3])
            #prediction
            daily_predicton_df = ml_model_of_suffix.create_df_of_daily_prediction_for_all_stocks_under_this_suffix()
            stock_prediction_df_lst.append(daily_predicton_df)

        ####
        #### now to generate 4 dfs, hist_acc, hist_recall, last_10d_acc, last_10d_recall
        #### for all models of different suffix, 
        #### 

        model_hist_acc_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), hist_acc_df_lst)
        model_hist_recall_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), hist_recall_df_lst)
        model_last_10d_acc_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), last_10d_acc_df_lst )
        model_last_10d_recall_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), last_10d_recall_df_lst )
        #prediction
        model_daily_prediction_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='Nasdaq_code', how="inner"), stock_prediction_df_lst )


        #### saving them as file
        lst_of_the_4_df = [model_hist_acc_df, model_hist_recall_df, model_last_10d_acc_df, model_last_10d_recall_df]
        lst_of_the_4_val = ["hist_acc", "hist_recall", "last_10d_acc", "last_10d_recall"]
        lst_of_the_4_df_name = [ v + "_df" for v in lst_of_the_4_val ]

        for i in range(0,4):
            df_i = lst_of_the_4_df[i]
            df_i_name = lst_of_the_4_df_name[i]
            df_i.to_csv(today_daily_prediction_work_dir + df_i_name + ".csv")
        
        #prediction
        model_daily_prediction_df.to_csv(today_daily_prediction_work_dir + "prediction.csv")


    






    