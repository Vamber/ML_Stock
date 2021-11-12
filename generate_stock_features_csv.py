from Download.google_trend_downloader import google_trend_downloader
from Download.google_news_downloader import google_news_downloader
from Download.stock_price_downloader import stock_price_downloader

from os import path
import os
import pandas as pd

import sys


##################
#
# The purpose of this python script to create command-line experience 
# for adding new stock and its feature into the stock_and_features.csv
# without the need to hand open stock_and_features.csv for mannual writting 
# 
# this method also has the advantage for the eventual automation and also formating checking
# so that you don't have a row with illegal arguments which would break the entire process. 
#
##################


####things to work on
# Ability to check redundance in of Nasdaq code
# sanity check for Nasdaq code, google trend, google news

program_name = "generate_stock_features_csv.py"
df_path = "Data/stock_and_features.csv"







  ##
    # This function is important, because it will be used by gnerate_stock_features_csv.py
    # For example if I want the google trend for the keyword RTX 3090 on day 2018-2-18
    # But RTX 3090 was not even out yet, there will just be no data on 2018-2-18
    # This means I can't have 3090 as a feature if default date is 2018-2-18
    # 
    ## 

def sanity_check_for_feature_of_stock(Nasdaq_code, default_date, google_trend_kw_lst_str, news_kw_lst_str):

    f = lambda result: "PASSED" if result else "FAILED"
    results = []
    print("Verifying the inserted stock & its features")
    #testing if Nasdaq_code is actually valid:
    verify_func = stock_price_downloader.sanity_check_if_keyword_has_data_on_default_start_date()
    result = verify_func(Nasdaq_code) is not None
    results.append(result)
    print("Nasdaq_code " + Nasdaq_code + " validity check:  " + f(result))

    #verifying trends kw
    verify_func = google_trend_downloader.sanity_check_if_keyword_has_data_on_default_start_date()
    google_trend_kw_lst = google_trend_kw_lst_str.strip(("[")).strip("]").split(",")
    for trend_kw in google_trend_kw_lst:
        result = verify_func(Nasdaq_code, default_date, trend_kw) is not None 
        results.append(result)
        print("Google trend kw " + trend_kw + " validty check: " + f(result) )
    

    #verifying news kw
    verify_func = google_news_downloader.sanity_check_if_keyword_has_data_on_default_start_date()
    news_kw_lst = news_kw_lst_str.strip("[").strip("]").split(",")
    for news_kw in news_kw_lst:
        result = verify_func(Nasdaq_code, default_date, news_kw) is not None
        results.append(result)
        print("news kw " + news_kw + " validty check: " + f(result) )


    return all(results)

    



def append_new_stock_and_features_to_csv(Nasdaq_code, default_date, google_trend_kw_lst, news_kw_lst):

    if not path.exists(df_path):
        empty_df = pd.DataFrame(columns=["Nasdaq_code", "start_date", "google_trend_kw_lst", "news_kw_lst"])
        empty_df.to_csv(df_path, index = False, index_label=False)


    Nasdaq_code = Nasdaq_code.strip("[").strip("]")
    default_date = default_date.strip("[").strip("]")


    sanity_check_success =  sanity_check_for_feature_of_stock(Nasdaq_code, default_date, google_trend_kw_lst, news_kw_lst)
    if not sanity_check_success:
        print("Attempt to insert " + Nasdaq_code + " Failed, please consider modifying inputs" )
        return False

    ### continues if the insertion is successful 
    df = pd.read_csv(df_path)
    new_row = {"Nasdaq_code": Nasdaq_code, 
               "start_date" : default_date, 
               "google_trend_kw_lst" : google_trend_kw_lst, 
               "news_kw_lst" : news_kw_lst}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(df_path, index = False)
    return True
    



if __name__ == "__main__":

    cmd_arg = sys.argv  
    print(len(cmd_arg))

    if len(cmd_arg) == 2 and cmd_arg[1] == "--help":
        print("for details, perform python3 " + program_name + " --help" + "  <option>")
        print("possible options:")
        print("add : for adding a new stock into csv")
        

    elif len(cmd_arg) == 3 and cmd_arg[1] == "--help":
        if cmd_arg[2] == "add":
            print("To insert a new stock to ML_stock auto data download and analysis:")
            print("Enter in the format:")
            print("python3" + program_name + " add [Nasdaq_code] [first_day_dwload_data] [google_trend_kw_1, google_trend_kw_2, ...] [news_kw1, news_kw-2, ...]")
            print("")
            print("eg:")
            print('python3 generate_stock_features_csv.py add [NVDA] [2019-2-14] "[buy nvidia stock, sell nvidia stock, nvidia stock, nvidia, amd]" "[nvidia, nvidia stock]"')

    elif len(cmd_arg) == 6 and cmd_arg[1] == "add":
        #### correct number of argument, starting checking the format ######
        for i in range(2, 6):
            arg_i = cmd_arg[i]
            if arg_i[0] != "[" or arg_i[-1] != "]":
                print(arg_i)
                print("invalid format ")
                print("try" + "python3 " + program_name + " --help")
                break
        
        #checking passed
        append_attempt = append_new_stock_and_features_to_csv(cmd_arg[2], cmd_arg[3], cmd_arg[4], cmd_arg[5])
        if append_attempt:
            print("now stock_and_features.csv is :")
            df = pd.read_csv(df_path)
            print(df)

    else:
        print("invalid format")
        print("try" + " python3 " + program_name + " --help")

