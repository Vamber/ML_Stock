


###
### provides series of readable APIs to collectively achieve the purpose of README.md 
###
import os 
from os import path
from datetime import date
import pandas as pd
import numpy as np
from Utils.good_trend_kw_filter_utils import good_trend_kw_filter 
from Download.google_trend_downloader import google_trend_downloader
from generate_stock_features_csv import append_new_stock_and_features_to_csv
from generate_stock_features_csv import delete_stock_from_csv
import random 


ROOT = "/home/vamber/ML_stock/"
df_dir = ROOT + "/Data/ML_Models/Daily_Prediction/"

def exec_cmd(cmd):
    res = os.system(cmd)
    if res != 0:
        print("Having issue executing " + cmd)
        exit(1)

def get_yesterday(date):
    return str(pd.Timestamp(date) - pd.Timedelta(1)).split(' ')[0]

##
## iteratively find the most recent report on hist_df
def get_n_stocks_with_lowest_acc_and_highest_recall(n):
    
    most_recent_day = str(date.today())
    while (not path.exists(df_dir + most_recent_day)):
        most_recent_day = get_yesterday(most_recent_day)

    recent_df_dir = df_dir + most_recent_day + "/"

    ret_stock_lst = []
    #
    hist_acc_df = pd.read_csv(recent_df_dir + "hist_acc_df.csv")
    hist_acc_df["avg_acc"] = hist_acc_df.iloc[:, 2:].apply(np.mean, axis=1)
    hist_acc_df = hist_acc_df[["Nasdaq_code", "avg_acc"]]
    hist_acc_df = hist_acc_df.sort_values(by="avg_acc")
    #
    ret_stock_lst += list(hist_acc_df["Nasdaq_code"])[0:n]

    #
    hist_recall_df = pd.read_csv(recent_df_dir + "hist_recall_df.csv")
    hist_recall_df["avg_recall"] = hist_recall_df.iloc[:, 2:].apply(np.mean, axis=1)
    hist_recall_df = hist_recall_df[["Nasdaq_code", "avg_recall"]]
    hist_recall_df = hist_recall_df.sort_values(by="avg_recall", ascending=False)
    ret_stock_lst += list(hist_recall_df["Nasdaq_code"])[0:n]
    
    #in case of redundancy
    ret_stock_lst = list(set(ret_stock_lst))

    return ret_stock_lst


#some helper function
###
###
def get_row_of_stock(Nasdaq_code):
    df_stocks = pd.read_csv(ROOT + "Data/stock_and_features.csv")
    row = df_stocks[df_stocks["Nasdaq_code"] == Nasdaq_code]
    return row.iloc[0]

def str_to_lst(string):
    return string.strip("[").strip("]").split(",")

def get_trend_kw_lst(row_of_stock):
    return str_to_lst(row_of_stock["google_trend_kw_lst"])

def get_news_kw_lst(row_of_stock):
    return str_to_lst(row_of_stock["news_kw_lst"])

def get_default_date(row_of_stock):
    return row_of_stock["start_date"]

###
###



# 1. it first collect a list of relevant kw suggest by google trend (which should be sorted automatically)
# 2. for each one of them, verify if we can actually download it since starting date 
#

def suggest_trend_kw_base_on_existing_kw(Nasdaq_code, starting_date, existing_kw):

    #remember, it's a dictionary, mapping the kw to its heuristical correlation value
    suggested_kw_lst = good_trend_kw_filter(Nasdaq_code, existing_kw)
    print(suggested_kw_lst)

    # loading the verification function
    verify_func = google_trend_downloader.sanity_check_if_keyword_has_data_on_default_start_date()
    #
    ret_kw_lst = []
    for sugg_kw_pair in suggested_kw_lst:
        sugg_kw = sugg_kw_pair[0]
        # ideally keep the word short
        if len(sugg_kw.split(" ")) > 2:
            pass
        else:
            result = verify_func(Nasdaq_code, starting_date, sugg_kw) is not None
            if result:
                ret_kw_lst.append(sugg_kw)
        # 3 kw maximum
        if len(ret_kw_lst) >= 3:
            break

    return ret_kw_lst


#
#
# 


##
## return a boolean value weather this stock was able to relearn features
##

def relearn_features_for_stock(Nasdaq_code):

    ##
    ## We don't need to relearn ^IXIC, it's there to provide information for other features
    if Nasdaq_code == "^IXIC":
        return False


    row_of_stock = get_row_of_stock(Nasdaq_code)
    g_news_lst = get_news_kw_lst(row_of_stock)
    g_trend_lst = get_trend_kw_lst(row_of_stock)
    start_date = get_default_date(row_of_stock)

    ##
    ## Init_log_file
    today = str(date.today())
    log_dir = ROOT + "/Data/Log/ReLearn/"
    if not path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = log_dir + today + ".txt"


    
    res = delete_stock_from_csv(Nasdaq_code)
    if res:
        exec_cmd( " echo " + Nasdaq_code + " deleted " + " >> " + log_file)
        exec_cmd( " echo " + str(list(row_of_stock)) + " was the old features " + " >> " + log_file)
    else:
        pass

    ##
    ##
    ## take 3 suggestion branching out from the google news
    suggest_1_lst = suggest_trend_kw_base_on_existing_kw(Nasdaq_code, start_date, random.choice(g_news_lst))
    ##
    ##
    ## take 3 suggestion branch out from an random trend_kw
    suggest_2_lst = suggest_trend_kw_base_on_existing_kw(Nasdaq_code, start_date, random.choice(g_trend_lst))
    ##
    ##
    new_trend_features = []
    suggest_1_n_2_lst = list(set(suggest_1_lst + suggest_2_lst))
    
    #
    # pick 3 random new good kw and add them into there 
    while (len(new_trend_features) < 3 and len(new_trend_features) < len(suggest_1_n_2_lst)):
        rand_pick = random.choice(suggest_1_n_2_lst)
        if rand_pick not in new_trend_features:
            new_trend_features.append(rand_pick)

    ##
    ## now actually inserting the stock with the new features
    ## we give it three tries, since this could be inconsistent
    res = False
    attemp = 3 
    while (not res and attemp > 0):
        res = append_new_stock_and_features_to_csv(Nasdaq_code, 
                                                start_date, 
                                                str(new_trend_features).replace("'", ""), 
                                                str(g_news_lst).replace("'", "")
                                                )
        attemp -= 1
    

    if res:
        exec_cmd( " echo " + Nasdaq_code + " updated " + " >> " + log_file)
        return True
    else:
        exec_cmd(" echo " + Nasdaq_code + " FAILED to update " + " >> " + log_file)







    



