




#
# This class intends to provide the template for all types of models that can be used to make prediction
#
# just like feature downloader, every instiation of ml_model (SVM, Linear Regression, Logistic Regression, LSTM) combined with its own feature engineering
#
# all needs to satisfy this template of ml_model
#
#
import os
from os import path
import pandas as pd
from datetime import date
from datetime import timedelta
from sklearn.model_selection import train_test_split as ts
import numpy as np
from joblib import dump, load

from functools import reduce

class ml_model_template():

    def __init__(self, model_name, model_suffix):
        self.name = model_name
        self.suffix = model_suffix
        self.train_ratio = 0.8
        self.test_ratio = 0.2
        self.training_termination_accuracy_threshold = 0.65
        self.ROOT = "/home/vamber/ML_stock/"
        #share_dir stores informations that can be shared by all models ofthe same type with different suffix
        self.share_dir = self.ROOT + "Data/ML_Models/" + "share_dir" + "/"
        self.work_dir = self.ROOT + "Data/ML_Models/" + self.model_name() + "/" + self.model_suffix() + "/"
        
        
        if not path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        self.daily_log_dir = self.work_dir + "/Daily_Prediction/"
        if not path.exists(self.daily_log_dir):
            os.makedirs(self.daily_log_dir)

        self.iter_5d_sim_log_dir = self.work_dir + "/Iter_5d_sim_log_dir/"
        if not path.exists(self.iter_5d_sim_log_dir):
            os.makedirs(self.iter_5d_sim_log_dir)

        self.fitted_model_dir = self.work_dir + "/" + "Fitted_Models" + "/"
        if not path.exists(self.fitted_model_dir):
            os.makedirs(self.fitted_model_dir)





    def model_name(self):
        return self.name

    def model_suffix(self):
        return self.suffix


    ###
    ### The most important function in which the child needs to inherit
    ### it return 2 d list
    ### return [ fitted_model, [training_score, test_score, recall, term_i]]
    ### this is a crucially important function that needs to be used by many template method
    ###
    def train_model_util(self, X_train, X_test, y_train, y_test, weight_vec):
        raise Exception("Critical !!!!", "train_model_util not is not imlement in child class, huge issue")

   


    # a very important function which needs to be used by iterative_5d_sim()
    # it must return a lst of 4 items
    # [train_acc, test_acc, recall, term_i]
    def train_model_and_predict_on_y_test(self, X_train, X_test, y_train, y_test, weight_vec):
        return self.train_model_util(X_train, X_test, y_train, y_test, weight_vec)[1]

    
    ##
    ## This function trains the model on the entire historical dataset and serialize it in its correspoding directory
    def train_model_and_save(self, Nasdaq_code):
        mega_feature_df = self.get_cached_mega_feature_df(Nasdaq_code)
        #setting test_n = 0 means to train on the entire dataset
        X_train, X_test, y_train, y_test, weight_vec = self.get_5_components_for_training_model(mega_feature_df, test_n=0)
        #
        fitted_model = self.train_model_util(X_train, None, y_train, None, weight_vec)[0]
        #
        self.save_fitted_model(Nasdaq_code, fitted_model)

        msg = self.name + " " + self.suffix
        print(msg + (40-len(msg))*" " + "Training" + "     " + Nasdaq_code)


    ##
    def save_fitted_model(self, Nasdaq_code, fitted_model):
        file_name = self.fitted_model_dir + Nasdaq_code + ".joblib"
        dump(fitted_model, file_name)

    ##
    def load_fitted_model(self, Nasdaq_code):
        file_name = self.fitted_model_dir + Nasdaq_code + ".joblib"
        if not path.exists(file_name):
            raise Exception("can not find a serialized model for" + Nasdaq_code + self.suffix + self.name + " program has a bug")
        fitted_model = load(file_name)
        return fitted_model


    # the idea is acutally simple
    # if the yesterday is missing in truncated_mega_feature_df
    # or there is Nan present in the row 
    # or yesterday is Friday or Saturday ..
    # then we don't predict 
    def can_predict_stock_today(self, truncated_mega_feature_df, yesterday):

        #HACK
        if yesterday not in list(truncated_mega_feature_df["date"]):
            return False
        else:
            yesterday_row = truncated_mega_feature_df[truncated_mega_feature_df["date"] == yesterday].iloc[0]
            yesterday_row = yesterday_row.drop(labels=["open_y", "close_y"])
            day_of_week = yesterday_row["day_of_week"]            
            #if yesterday is Friday, then we shouldn't predict stocks
            if day_of_week == 5:
                return False
            else:
                #the next round of filtering
                #we allow the stock price feature to be na if yesterday is Sunday
                if day_of_week == 6:
                    yesterday_row = yesterday_row.drop(labels=[i for i in yesterday_row.index if "open" in i or "close" in i or "Nasdaq_market" in i])
                is_missing_values = yesterday_row.isnull().values.any()
                return not is_missing_values

        


    def predict_stock(self, Nasdaq_code):

        truncated_mega_feature_df = self.get_truncated_mega_feature_df(Nasdaq_code)
        yesterday = str(date.today() - timedelta(days=1))

        if not self.can_predict_stock_today(truncated_mega_feature_df, yesterday):
            return -777

        else:
            truncated_mega_feature_df = truncated_mega_feature_df.drop(columns=["open_y", "close_y"])
            X = self.feature_engineering(truncated_mega_feature_df)
            last_row = X.iloc[-1, :]
            last_row = last_row.to_numpy().reshape(1,-1)
            fitted_model = self.load_fitted_model(Nasdaq_code)
            prediction = fitted_model.predict((last_row))[0]
            ###
            msg = self.name + " " + self.suffix
            print(msg + (40-len(msg))*" "+ "Predicts" + "     " + Nasdaq_code + "      " + str(prediction))
            #
            return prediction 



    #see below for the definition of feature_engineering_base_on_suffix
    def feature_engineering(self, mega_feature_df):
        return self.feature_engineering_base_on_suffix(mega_feature_df, self.suffix)

    #see below to see the definition of get_4_components_for_training_model_helper
    # return X_train, X_test, y_train, y_test, train_weight_vec
    def get_5_components_for_training_model(self, mega_feature_df, test_n):
        return self.get_5_components_for_training_model_helper(mega_feature_df, test_n, self.suffix)


    #get a row object that corresponds this stock
    def get_row_of_stock(self, Nasdaq_code):
        df_stocks = pd.read_csv(self.ROOT + "Data/stock_and_features.csv")
        row = df_stocks[df_stocks["Nasdaq_code"] == Nasdaq_code]
        return row.iloc[0]



    #turn a stringfied lst back to an actual python lst
    def str_to_lst(self, string):
        return string.strip("[").strip("]").split(",")


    def get_trend_kw_lst(self, row_of_stock):
        return self.str_to_lst(row_of_stock["google_trend_kw_lst"])

    def get_news_kw_lst(self, row_of_stock):
        return self.str_to_lst(row_of_stock["news_kw_lst"])
    

    ###
    ### an extremely important function
    ###
    def get_mega_feature_df(self, Nasdaq_code, truncated=False):
        mega_news_df = self.get_mega_news_df(Nasdaq_code, truncated)
        mega_news_df_T = self.transpose_mega_news_df(mega_news_df)

        mega_stock_price_df_T = self.get_mega_stock_price_df(Nasdaq_code, truncated)

        ##
        ## Add the general nasdaq market closing price as a feature
        ##
        mega_Nasdaq_price_df_T = self.get_mega_stock_price_df("^IXIC", truncated)
        mega_Nasdaq_price_df_T = mega_Nasdaq_price_df_T.drop(columns=[c for c in mega_Nasdaq_price_df_T.columns if "open" in c])
        new_cols = {}
        for c in mega_Nasdaq_price_df_T.columns:
            if c != "date":
                new_cols[c] = ("Nasdaq_market_" + c).replace("close_", "")
        mega_Nasdaq_price_df_T = mega_Nasdaq_price_df_T.rename(columns=new_cols)
        mega_stock_price_df_T = pd.merge(mega_stock_price_df_T, mega_Nasdaq_price_df_T, on="date", how="inner")
        ##
        ##
        ##


        #this one is already transposed
        mega_trend_df_T = self.get_mega_trend_df(Nasdaq_code, truncated)

        #first downloaded_day
        first_day = mega_trend_df_T["date"].iloc[0]
        mega_stock_price_df_T = mega_stock_price_df_T[mega_stock_price_df_T["date"] >= first_day]
    

        #now, here is the catch, we first inner join trend + news
        #and then outer join with stock_price
        #the reason we need to do this is because, news+trend must coexist together for any form of prediction to happen
        news_n_trend = pd.merge(mega_news_df_T, mega_trend_df_T, on="date", how="inner")
        mega_feature_df = pd.merge(mega_stock_price_df_T, news_n_trend, on="date", how="outer")
        mega_feature_df = mega_feature_df.sort_values(by="date")

        # Also add in some more helperful features
        mega_feature_df["day_of_week"] = mega_feature_df["date"].apply(self.day_of_week)
    
        #open_y is the price tomorrow, it's called y because it's the predicted value
        open_y = list(mega_feature_df["open_m0"][1:]) + [mega_feature_df["open_m0"].iloc[-1]]

        #close_y is the closing price tomorrow,
        close_y = list(mega_feature_df["close_m0"][1:]) + [mega_feature_df["close_m0"].iloc[-1]]


        # y is the predicted value
        mega_feature_df["open_y"] = open_y
        mega_feature_df["close_y"] = close_y

        return mega_feature_df




    # mega_feature df is huge and it's computationally costly to calculate
    # therefore if we are just trying to predic the stock price for tomorrow
    # then we only need the last few rows, (the very last row to be precise)
    # therefore, we can just grab the last few rows for faster computation

    def get_truncated_mega_feature_df(self, Nasdaq_code):

        return self.get_mega_feature_df(Nasdaq_code, truncated=True)




    def create_and_store_mega_feature_df(self, Nasdaq_code):
        df = self.get_mega_feature_df(Nasdaq_code)
        stock_share_dir = self.share_dir + "/" + Nasdaq_code
        if not path.exists(stock_share_dir):
            os.makedirs(stock_share_dir)
        today = str(date.today())
        file_name = "mega_feature_df" + "#" + today + ".csv"
        file_path = stock_share_dir + "/" + file_name
        df.to_csv(file_path)

    def get_cached_mega_feature_df(self, Nasdaq_code):
        stock_share_dir = self.share_dir + "/" + Nasdaq_code
        if not path.exists(stock_share_dir):
            os.makedirs(stock_share_dir)
        today = str(date.today())
        file_name = "mega_feature_df" + "#" + today + ".csv"
        file_path = stock_share_dir + "/" + file_name
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            self.create_and_store_mega_feature_df(Nasdaq_code)
            return self.get_cached_mega_feature_df(Nasdaq_code)

        




###
### From this line and on wards, it's just bunch of helper function trying to help to create mega_df
### mega_df is a very complex df
###
### 

### this function create a mega_news_df 
### which contains the sentiment score + number of news for every news title for the past every single day
### it needs 4 helper fucntion which are defined immdiate below it
    def get_mega_news_df(self, Nasdaq_code, truncated):
        row_of_stock = self.get_row_of_stock(Nasdaq_code)
        news_kw_lst = self.get_news_kw_lst(row_of_stock)
    
        news_dfs = []
        for news_kw in news_kw_lst:
            dates_processed_lst = self.get_dates_processed_for_a_news_kw(Nasdaq_code, news_kw)
            if truncated:
                dates_processed_lst = dates_processed_lst[-14:]

            news_kw_df = self.get_news_df_of_kw_on_lst_of_dates(Nasdaq_code, news_kw, dates_processed_lst)
            news_kw_df = self.agg_news_df(news_kw_df, news_kw)
            news_dfs.append(news_kw_df)

        mega_news_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='date', how="inner"), news_dfs)

        return mega_news_df



## news helper 1 
    def get_dates_processed_for_a_news_kw(self, Nasdaq_code, kw):
        df_path = self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Raw_Features/Google_News/"+ kw + "/" + "dates_processed" + ".csv"
        df = pd.read_csv(df_path)
        df = df.sort_values(by="dates")
        return list(df["dates"])

## news helper 2
    def get_news_df_of_kw_on_date(self, Nasdaq_code, kw, date, keep_source=False):
        df_path = self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Google_News/"+ kw + "/" + date + ".csv"
        df = pd.read_csv(df_path)
        df["date"] = [date]*(max (df["total_news_today"].iloc[0], 1))
        df = df.rename(columns={"sentiment_score":kw + "_" + "sentiment_score",
                            "total_news_today": kw + "_" + "news_num"})

        if not keep_source:                      
            return df[["date",kw + "_" + "sentiment_score", kw + "_" + "news_num"]]
        else:
            return df[["date",kw + "_" + "sentiment_score", kw + "_" + "news_num", "source", "title"]]

## news helper 3
    def get_news_df_of_kw_on_lst_of_dates(self, Nasdaq_code, kw, lst_date, keep_source=False):
        news_df = []
        for date in lst_date:
            if not keep_source:
                news_df.append(self.get_news_df_of_kw_on_date(Nasdaq_code, kw, date))
            else:
                news_df.append(self.get_news_df_of_kw_on_date(Nasdaq_code, kw, date, keep_source=True))

        mega_df = pd.concat(news_df)
        return mega_df


## news helper 4
    def agg_news_df(self, news_df, kw):
        df = news_df[["date", kw + "_news_num", kw + "_" + "sentiment_score"]]
        ret_df = df.groupby("date").mean()
        ret_df[kw + "_" + "sentiment_score_max"] = df.groupby("date").max()[kw + "_" + "sentiment_score"]
        ret_df[kw + "_" + "sentiment_score_min"] = df.groupby("date").min()[kw + "_" +"sentiment_score"]
        ret_df = ret_df.reset_index()
        return ret_df


####
#### The current mega_news_df is not yet transpose, we still need to transpose it
#### notice, the tranpose mega_news_df is actually quite large, around 50 columns
#### 
    def transpose_mega_news_df(self, mega_news_df):
        og_cols = list(mega_news_df.columns)
        #remove date temporarily, because we don't want date_m0, date_m1, date_m2
        og_cols.remove("date")
        prev_dates = ["_m0", "_m1", "_m2", "_m3", "_m4", "_m5", "_m6"]

        col_with_prev_dates = []
        for c in og_cols:
            col_with_prev_dates.append([c + i for i in prev_dates])

        # turn the 2d lst into 1d lst
        col_with_prev_dates = sum(col_with_prev_dates, [])
        # adding the date column back 
        col_with_prev_dates = ["date"] + col_with_prev_dates

        df_T = pd.DataFrame(columns=col_with_prev_dates)
        df = mega_news_df

        for i in range(7, len(df)+1):
            df_m6 = df.iloc[i-7:i, :]
            date = df_m6["date"].iloc[-1]
            row = []
            for c in og_cols:
                c_lst_m6 = list(df_m6[c])
                c_lst_m6.reverse()
                row.append(c_lst_m6)
            #flatten the row
            row = sum(row, [])
            row = [date] + row
            df_T.loc[i-7] = row

        return df_T
    



#### this function creates the mega trend df, every row is date
#### every date contains the kw_trend values for the past 7 days
####
#### This function also needs 5 helper functions

    def get_mega_trend_df(self, Nasdaq_code, truncated):
        row_of_stock = self.get_row_of_stock(Nasdaq_code)
        trend_kw_lst = self.get_trend_kw_lst(row_of_stock)

        trend_dfs = []
        for trend_kw in trend_kw_lst:
            dates_processed_lst = self.get_dates_processed_for_a_trend_kw(Nasdaq_code, trend_kw)
            if truncated:
                dates_processed_lst = dates_processed_lst[-14:]
            trend_kw_df = self.get_transposed_trend_df_of_kw_from_lst_of_dates(Nasdaq_code, trend_kw, dates_processed_lst)
            trend_dfs.append(trend_kw_df)

        mega_trend_df = reduce(lambda df1,df2: pd.merge(df1,df2,on='date', how="inner"), trend_dfs)

        return mega_trend_df


## trend helper #1 
    def get_dates_processed_for_a_trend_kw(self, Nasdaq_code, kw):
        df_path = self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Raw_Features/Google_Trends/"+ kw + "/" + "dates_processed" + ".csv"
        df = pd.read_csv(df_path)
        df = df.sort_values(by="dates")
        return list(df["dates"])

## trend helper #2
    def get_trend_df_of_kw_on_date(self, Nasdaq_code, kw, date):
        df_path = self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Google_Trends/"+ kw + "/" + date + ".csv"
        df = pd.read_csv(df_path)
        df = df.rename(columns={"only_day": "date"})
        return df

## trend helper #3
    def transpose_google_trend_df(self, trend_df, kw, date):
        prev_dates = ["_m0", "_m1", "_m2", "_m3", "_m4", "_m5", "_m6"]
        prev_dates = [kw + i for i in prev_dates]
        df_cols = ["date"] + prev_dates
        trend_sc_lst = list(trend_df[kw])
        trend_sc_lst.reverse()
        df_vals = [date] + trend_sc_lst
        col_val_dic = {}
        for i in range(0, 8):
            col_val_dic[df_cols[i]] = df_vals[i]
    

        df = pd.DataFrame(col_val_dic, index=[0])
        return df

## trend helper #4
    def get_transposed_trend_df_of_kw_on_date(self, Nasdaq_code, kw, date):
        df = self.get_trend_df_of_kw_on_date(Nasdaq_code, kw, date)
        df_T = self.transpose_google_trend_df(df, kw, date)
        return df_T

## trend helper #5
    def get_transposed_trend_df_of_kw_from_lst_of_dates(self, Nasdaq_code, kw, lst_of_date):
        trend_df = []
        for date in lst_of_date:
            trend_df.append(self.get_transposed_trend_df_of_kw_on_date(Nasdaq_code, kw, date))
        semi_mega_df = pd.concat(trend_df)
        return semi_mega_df


####
#### this function creates the mega_stock_price_df
#### row each is a date, and the closing+opening price for the last 7 days
####
####

    def get_mega_stock_price_df(self, Nasdaq_code, truncated):
        df = self.get_stock_price_df(Nasdaq_code, truncated)
        prev_dates = ["_m0", "_m1", "_m2", "_m3", "_m4", "_m5", "_m6"]
        col_open = ["open" + i for i in  prev_dates]
        col_close = ["close" + i for i in prev_dates]
        col = ["date"] + col_open + col_close
        df_T = pd.DataFrame(columns=col)

        for i in range(7, len(df)+1):
            df_m6 = df.iloc[i-7:i, :]
            date = df_m6["date"].iloc[-1]
            open_lst_m6 = list(df_m6["open"])
            close_lst_m6 = list(df_m6["close"])
            open_lst_m6.reverse()
            close_lst_m6.reverse()
            row = [date] + open_lst_m6 + close_lst_m6
            df_T.loc[i-7] = row

        return df_T


    def get_stock_price_df(self, Nasdaq_code, truncated):
        df_path = self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Stock_Price/price.csv"
        start = 2000
        df = pd.read_csv(df_path)
        start = 0
        if len(df) >= 2000:
            start = -2000

        df = df.rename(columns={"Date": "date", "Open":"open", "Close":"close"})
        if truncated:
            start = -14

        return df.iloc[start:][["date", "open", "close"]]


####
#### some misslanues helper functions
####
####
    #if today is Sunday(7), then tomorrow is Monday
    def day_of_week(self, date_str):
        return pd.Timestamp(date_str).dayofweek
 








###########
###########
########### From this line and below, it is all functions related to mega_feature_df
###########
###########

    def ffill_and_dropna(self, mega_feature_df):
        df = mega_feature_df

        #the following if and else is a pretty ugly WAR I have
        if "open_y" in list(df.columns):
            df_no_weekend = df[df["open_y"]> 0]
        else:
            df_no_weekend = df

        df_no_weekend = df_no_weekend.fillna(method="ffill")
        df_no_weekend = df_no_weekend.dropna()
        return df_no_weekend


    #remove things such as like the weekdays, dates,  and stuffs that can't be turned into a numerical matrix 

    def remove_non_mx_features(self, mega_feature_df):
        df = mega_feature_df
        cols = list(df.columns)
        mx_lst = ["_m0", "_m1", "_m2", "_m3", "_m4", "_m5", "_m6"]
        col_mx = [c for c in cols if any([i in c for i in mx_lst])]
        df = df[col_mx]
        return df



    def std_mega_feature_df(self, mega_feature_df):
        df = mega_feature_df
        cols = list(df.columns)
        mx_lst = ["_m0", "_m1", "_m2", "_m3", "_m4", "_m5", "_m6"]
        col_mx = [c for c in cols if any([i in c for i in mx_lst])]
        df = df[col_mx].copy()

        assert len(col_mx) % 7 == 0, "series bug occured with get mega_feature_fd"

        for i in range(0, len(col_mx), 7):
            df_sub_section = df.iloc[:, i:i+7]
            #the next two line normalize the sub_df by row
            df_sub_section = df_sub_section.sub(df_sub_section.mean(axis=1), axis=0)
            df_sub_section = df_sub_section.div(df_sub_section.std(axis=1), axis=0)
            #replace the df_by this section
            df.iloc[:, i:i+7] = df_sub_section

        df =df.fillna(0)
        return df




    def std_n_diff_mega_feature_df(self, mega_feature_df):
        std_df = self.std_mega_feature_df(mega_feature_df)
        for i in range(0, std_df.shape[1] - 1):
            col_i = std_df.iloc[:, i]
            col_ip1 = std_df.iloc[:, i+1]
            std_df.iloc[:, i] = col_i - col_ip1
        std_df = std_df.drop(columns=[c for c in list(std_df.columns) if "_m6" in c ] )
        return std_df

    #removes number of features for dimension reduction
    def dimension_reduction(self, mega_feature_df, xm_to_remove):
        n = xm_to_remove
        assert n <= 6, "xm to remove is greater than 6, you are removing all features, STOP !"
        m_lst = ["_m6", "_m5", "_m4", "_m3", "_m2", "_m1"]
        m_lst = m_lst[0:n]

        mega_feature_df = mega_feature_df.drop(columns=[i for i in list(mega_feature_df.columns) if any([ j for j in m_lst if j in i]) ] )

        return mega_feature_df


    def add_tmr_mday_col(self, df, day_of_week_lst):
        df["tmr_mday"] = [(i==6)*1 for i in day_of_week_lst]
        return df


    # ["sentiment_score_m", "sentiment_score_max_m"] into ["sentiment_score_m0", "sentiment_score_max_m0", ["sentiment_score_m1", "sentiment_score_max_m1"]] .....
    def add_m0_2_m6_at_end(self, lst):
        res = []
        for w in lst:
            for i in range(0,7):
                res.append(w+str(i))
        return res


    def feature_selection(self, mega_feature_df, bit):
        bit_map = { 0 : [], 
                1 : self.add_m0_2_m6_at_end(["sentiment_score_m", "sentiment_score_max_m"]), 
                2 : self.add_m0_2_m6_at_end(["sentiment_score_m", "sentiment_score_min_m"]), 
                3 : self.add_m0_2_m6_at_end(["sentiment_score_max_m", "sentiment_score_min_m"]), 
                4 : self.add_m0_2_m6_at_end(["sentiment_score_m"])
                }

        cols_to_drop = bit_map[bit]

        mega_feature_df = mega_feature_df.drop(columns=[c for c in mega_feature_df.columns if any([i for i in cols_to_drop if i in c])])

        return mega_feature_df


    def add_price_delta_and_drop_open_close(self, mega_feature_df):
        open_cols = [c for c in mega_feature_df.columns if "open_m" in c ]
        close_cols = [c for c in mega_feature_df.columns if "close_m" in c ]

        df_open = mega_feature_df.loc[:, open_cols].to_numpy()
        df_close = mega_feature_df.loc[:, close_cols].to_numpy()


        df_price_delta = df_close -  df_open

    
        n = df_price_delta.shape[1]
        delta_cols = ["price_delta_m" + str(i) for i in range(0,n)]

        mega_feature_df = mega_feature_df.drop(columns=open_cols+close_cols)

        mega_feature_df.loc[:, delta_cols] = df_price_delta

        return mega_feature_df


    def create_weight_vector(self, df):
        n = len(df)
        return np.array([i/n for i in range(1, n+1)])


    def add_weight_by_price_delta(self, og_weight_vec, price_ratio_vec):
        price_ratio_vec = price_ratio_vec[0:len(og_weight_vec)]
        price_ratio_vec = np.array(price_ratio_vec)
        delta = ((price_ratio_vec - 1)*50)**2
        #scale everything back to 1
        delta = (delta/max(delta))*2
        og_weight_vec = og_weight_vec + delta
        return og_weight_vec


    def feature_engineering_base_on_suffix(self, mega_feature_df, suffix):
        
        #check the README.md for what each represents in this module
        bit_0 = int(suffix[0])
        bit_1 = int(suffix[1])
        bit_2 = int(suffix[2])
        bit_3 = int(suffix[3])

        df = mega_feature_df

        df = self.ffill_and_dropna(df)

        #deciding if to add price_delta
        if bit_3 == 1:
            df = self.add_price_delta_and_drop_open_close(df)

        
        
        if bit_1 == 0:
            X = self.remove_non_mx_features(df)

            
        elif bit_1 == 1:
            X = self.std_mega_feature_df(df)
        elif bit_1 == 2:
            X = self.std_n_diff_mega_feature_df(df)
        

        #handling dimentionality reduction
        X = self.dimension_reduction(X, bit_0)

        #handling feature selection
        X = self.feature_selection(X, bit_2)

        #add if tomorrow is Monday
        X = self.add_tmr_mday_col(X, df["day_of_week"])

        return X




    




########
########
######## a helper function that creates X_train
########
########
    def get_5_components_for_training_model_helper(self, mega_feature_df, test_n, suffix):

        weight_bit = int(suffix[4])

        X = self.feature_engineering(mega_feature_df)
        df = self.ffill_and_dropna(mega_feature_df)
        y = (df["close_y"] - df["open_y"]).apply(lambda x: 1 if x > 0 else -1)

        #CRITICAL: setting shuffle is false is hugely important, because we will be using past to predict future
        if test_n == 0:
            X_train,X_test,y_train,y_test = X, None, y, None
        else:
            X_train,X_test,y_train,y_test = ts(X,y,test_size=test_n, shuffle=False)

        #creating weight vector
        if weight_bit == 0:
            weight_vector = []
        elif weight_bit == 1:
            weight_vector = self.create_weight_vector(X_train)
        elif weight_bit == 2:
            weight_vector = self.create_weight_vector(X_train)
            weight_vector = self.add_weight_by_price_delta(weight_vector, df["close_y"]/df["open_y"])


        return [X_train,X_test,y_train,y_test,weight_vector]




######## 
######## 
######## this function is used for running iterative 5 day simulation
######## therefore the test size is set to 5 as a constant
########
    def get_5_components_for_training_model_for_5d_iterative_sim(self, mega_feature_df, iter_n):
        suffix = self.suffix
        weight_bit = int(suffix[4])

        X = self.feature_engineering(mega_feature_df)
        X_total_rows = len(X)
        end_row = X_total_rows - 100
        
        #the end row has to do with the number of iteration
        end_row = end_row + (iter_n+1)*5

        X = X.iloc[0:end_row, : ]

        df = self.ffill_and_dropna(mega_feature_df)
        y = (df["close_y"] - df["open_y"]).apply(lambda x: 1 if x > 0 else -1).iloc[:end_row]

        #CRITICAL: setting shuffle is false is hugely important, because we will be using past to predict future
        X_train,X_test,y_train,y_test = ts(X,y,test_size=5, shuffle=False)

        #creating weight vector
        if weight_bit == 0:
            weight_vector = []
        elif weight_bit == 1:
            weight_vector = self.create_weight_vector(X_train)
        elif weight_bit == 2:
            weight_vector = self.create_weight_vector(X_train)
            weight_vector = self.add_weight_by_price_delta(weight_vector, df["close_y"]/df["open_y"])


        return [X_train,X_test,y_train,y_test,weight_vector]


    #v_recall is the terminology that describes the situation in which stock is went down, but the model predict the stock went up
    # false positive / total negative
    def v_recall(self, y_true, y_pred):
        y_true = list(y_true)
        y_pred = list(y_pred)
        n = len(y_true)
        lose = 0
        lose_and_buy = 0
        for i in range(0,n):
            if y_true[i] == -1:
                lose +=1
                if y_pred[i] == 1:
                    lose_and_buy +=1
        if lose == 0:
            return 0 
        
        return lose_and_buy / lose
    
    
#########
#########
#########
#########
    def run_iterative_5d_sim_on_stock_dataset(self, Nasdaq_code):

        mega_feature_df = self.get_cached_mega_feature_df(Nasdaq_code)
        iter_i_lst = []
        train_acc_lst = []
        test_acc_lst = []
        recall_lst = []
        for i in range(0,20):
            #
            X_train, X_test, y_train, y_test, weight_vec = self.get_5_components_for_training_model_for_5d_iterative_sim(mega_feature_df, i)
            #
            train_acc, test_acc, recall, term_i = self.train_model_and_predict_on_y_test(X_train, X_test, y_train, y_test, weight_vec)
            #
            iter_i_lst.append(i)
            train_acc_lst.append(train_acc)
            test_acc_lst.append(test_acc)
            recall_lst.append(recall)
        
        print(self.name + " " + self.suffix + " " + Nasdaq_code)
        print("the average testing accracy is :")
        print(np.mean( np.array(test_acc_lst)   ))
        

        ## save data
        iter_5d_sim_log_file = self.iter_5d_sim_log_dir + Nasdaq_code + ".csv"
        df = pd.DataFrame({"iter_i" : iter_i_lst, 
                          "train_acc" : train_acc_lst, 
                          "test_acc" : test_acc_lst, 
                          "recall" : recall_lst})

        df.to_csv(iter_5d_sim_log_file)


#########
######### the 4 values are respectively: hist_acc, hist_recall, last_10d_acc, last_10d_recall 
#########
######### they are really important in terms of the formation of the final output of the module, which are 5 data_frames to be handed into the Expert module
#########
    def get_4vals_of_acc_and_recall_from_iterative_5d_sim_log(self, Nasdaq_code):

        iter_5d_sim_log_file = self.iter_5d_sim_log_dir + Nasdaq_code + ".csv"
        
        #not sure why this file will not exist, but if it doesn't, represent the missing value with -1
        if not path.exists(iter_5d_sim_log_file):
            return [-1,-1,-1,-1]

        else:
            sim_log_df = pd.read_csv(iter_5d_sim_log_file)
            hist_acc = np.mean( sim_log_df["test_acc"].to_numpy() )
            hist_recall = np.mean(  sim_log_df["recall"].to_numpy() )
            #it's only the last two items becauses each item is 5 days
            last_10d_acc = np.mean( sim_log_df["test_acc"].to_numpy()[-2:] )
            last_10d_recall = np.mean( sim_log_df["recall"].to_numpy()[-2: ])

            return [hist_acc, hist_recall, last_10d_acc, last_10d_recall]


    #helper function for the following
    def get_nasdaq_code_lst(self):
        df_path = self.ROOT + "/Data/stock_and_features.csv"
        df = pd.read_csv(df_path)
        nasdaq_lst = list(df["Nasdaq_code"])
        return nasdaq_lst


########
######## generate 4 dfs of this model, this partcular suffix, for all nasdaq code,
######## hist_acc_df, hist_recall_df, last_10d_acc_df, last_10d_recall_df 
########

    def create_4dfs_of_acc_and_recall_for_all_stocks_under_this_suffix(self):

        df_work_dir = self.daily_log_dir + "/" + str(date.today()) + "/"
        if not path.exists(df_work_dir):
            os.makedirs(df_work_dir)

        nasdaq_2_4vals_map = {}

        nasdaq_lst = self.get_nasdaq_code_lst()
        for nasdaq in nasdaq_lst:
            nasdaq_2_4vals_map[nasdaq] = self.get_4vals_of_acc_and_recall_from_iterative_5d_sim_log(nasdaq)

        #init the 4 df
        hist_acc_df = pd.DataFrame(columns=["Nasdaq_code", "hist_acc"])
        hist_recall_df = pd.DataFrame(columns=["Nasdaq_code", "hist_recall"])
        last_10d_acc_df = pd.DataFrame(columns=["Nasdaq_code", "last_10d_acc"])
        last_10_recall_df = pd.DataFrame(columns=["Nasdaq_code", "last_10d_recall"])

        #just a quick way to fill in the value
        lst_of_the_4_df = [hist_acc_df, hist_recall_df, last_10d_acc_df, last_10_recall_df]
        lst_of_the_4_val = ["hist_acc", "hist_recall", "last_10d_acc", "last_10d_recall"]
        lst_of_the_4_df_name = [ v + "_df" for v in lst_of_the_4_val ]
        for i in range(0,4):
            #
            df_i = lst_of_the_4_df[i]
            df_i["Nasdaq_code"] = list(nasdaq_2_4vals_map.keys())
            #
            df_i_val = lst_of_the_4_val[i]
            df_i[df_i_val] = [ l[i] for l in nasdaq_2_4vals_map.values() ]
            #rename col
            df_i = df_i.rename(columns={df_i_val : self.model_name()+"_"+self.model_suffix()+"_"+df_i_val})
            lst_of_the_4_df[i] = df_i 
            #
            df_i_name = lst_of_the_4_df_name[i]
            df_i.to_csv(df_work_dir + df_i_name +".csv")

        return lst_of_the_4_df


    def create_df_of_daily_prediction_for_all_stocks_under_this_suffix(self):
        
        df_work_dir = self.daily_log_dir + "/" + str(date.today()) + "/"
        if not path.exists(df_work_dir):
            os.makedirs(df_work_dir)

        nasdaq_2_prediction_map = {}
        
        nasdaq_lst = self.get_nasdaq_code_lst()
        for nasdaq in nasdaq_lst:
            nasdaq_2_prediction_map[nasdaq] = self.predict_stock(nasdaq)
        
        #use variable col_1 to shorten 
        col_1 = self.name+"_"+self.suffix+"_"+"pred"
        pred_df = pd.DataFrame(columns=["Nasdaq_code", col_1 ])
        pred_df["Nasdaq_code"] = list(nasdaq_2_prediction_map.keys())
        pred_df[col_1] = list(nasdaq_2_prediction_map.values())
        pred_df.to_csv(df_work_dir + "/prediction.csv")
        return pred_df





        
        




        




    