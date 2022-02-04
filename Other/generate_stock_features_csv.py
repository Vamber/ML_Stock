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
ROOT = "/home/vamber/ML_stock/"
df_path = ROOT + "Data/stock_and_features.csv"







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
        downloaded_df = verify_func(Nasdaq_code, default_date, news_kw)
        result = downloaded_df is not None
        results.append(result)
        print("news kw " + news_kw + 
              " validty check: " + f(result) + 
              " (" + str(downloaded_df["total_news_today"][0]) + " news found on default date )")


    return all(results)




def checking_if_a_Nasdaq_code_exists_in_csv(Nasdaq_code):
    df = pd.read_csv(df_path)
    return Nasdaq_code in list(df["Nasdaq_code"])





def append_new_stock_and_features_to_csv(Nasdaq_code, default_date, google_trend_kw_lst, news_kw_lst):

    if not path.exists(df_path):
        #please be very cautious when modifying collumns, it could have dire consequences on the remaining dependencies. 
        empty_df = pd.DataFrame(columns=["Nasdaq_code", "start_date", "google_trend_kw_lst", "news_kw_lst"])
        empty_df.to_csv(df_path, index = False, index_label=False)


    Nasdaq_code = Nasdaq_code.strip("[").strip("]")
    default_date = default_date.strip("[").strip("]")
    google_trend_kw_lst = google_trend_kw_lst.replace(", ", ",")
    news_kw_lst = news_kw_lst.replace(", ", ",")

    if checking_if_a_Nasdaq_code_exists_in_csv(Nasdaq_code):
        print("Nasdaq_code :" + Nasdaq_code + " already exists in csv ")
        print("Insertion failed, please consider the update option")
        return False

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


def delete_stock_from_csv(Nasdaq_code):
    if not checking_if_a_Nasdaq_code_exists_in_csv(Nasdaq_code):
        print(Nasdaq_code + " is not found in stock_and_feature.csv " + ", no deletion performed")
        return False
    else:
        df = pd.read_csv(df_path)
        df = df[df.Nasdaq_code != Nasdaq_code]
        df.to_csv(df_path, index = False)
        print(Nasdaq_code + " has been deleted")
        return True




def display():
    df = pd.read_csv(df_path)
    print(df)


if __name__ == "__main__":

    cmd_arg = sys.argv  
    print(len(cmd_arg))

    if len(cmd_arg) == 2 and cmd_arg[1] == "--help":
        print("for details, perform python3 " + program_name + " --help" + "  <option>")
        print("possible options:")
        print("add : for adding a new stock into csv")
        print("delete : remove an existing row corresponding to one stock in stock_and_feature.csv")
        print("display : printing out the current stock_and_feature.csv ")

        
    ##
    # HELP
    ##
    elif len(cmd_arg) == 3 and cmd_arg[1] == "--help" and cmd_arg[2] in ["add", "display", "delete"]:
        if cmd_arg[2] == "add":
            print("To insert a new stock to ML_stock auto data download and analysis:")
            print("Enter in the format:")
            print("python3 " + program_name + " add [Nasdaq_code] [first_day_dwload_data] [google_trend_kw_1, google_trend_kw_2, ...] [news_kw1, news_kw-2, ...]")
            print("")
            print("eg:")
            print('python3 generate_stock_features_csv.py add [NVDA] [2019-2-14] "[buy nvidia stock, sell nvidia stock, nvidia stock, nvidia, amd]" "[nvidia, nvidia stock]"')
    
    ##
    # ADD
    ##
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
            display()
        else:
            #return non zero exit code 
            exit(1)

    ##
    # DELETE
    ##
    elif len(cmd_arg) == 3 and cmd_arg[1] == "delete":
        Nasdaq_code = cmd_arg[2].strip("[").strip("]")
        delete_stock_from_csv(Nasdaq_code)

    ##
    # DISPLAY
    ##
    elif len(cmd_arg) == 2 and cmd_arg[1] == "display":
        display()


    else:
        print("invalid format")
        print("try" + " python3 " + program_name + " --help")

