


import pandas as pd

day_m1_path = "/home/vamber/ML_stock/Data/Expert/expert_vamber/daily_choice/2022-01-24/"
day_m2_path = "/home/vamber/ML_stock/Data/Expert/expert_vamber/daily_choice/2022-01-21/"


m1_selection_df_path = day_m1_path + "stock_selection_lst.csv"


m2_selection_df_path = day_m2_path + "stock_selection_lst.csv"
m2_stocks_2_shares_df_path = day_m2_path + "stock_2_shares.csv"
m2_bank_saving = day_m2_path + "bank_saving.csv"




def test0():
    print("TESTING GENEAL CASE")
    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"], 
                       "shares" : [1, 2, 3]})
    df.to_csv(m2_stocks_2_shares_df_path, index=False)

    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"]})
    df.to_csv(m2_selection_df_path, index=False)

    df = pd.DataFrame({"bank_saving" : [0]})
    df.to_csv(m2_bank_saving, index=False)


    df = pd.DataFrame({ "Nasdaq_code" : ["BA", "BLK", "BMY"]})
    df.to_csv(m1_selection_df_path, index=False)


def test1():
    print("TESTING GENEAL CASE with stock over lapp")
    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"], 
                       "shares" : [1, 2, 3]})
    df.to_csv(m2_stocks_2_shares_df_path, index=False)

    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"]})
    df.to_csv(m2_selection_df_path, index=False)

    df = pd.DataFrame({"bank_saving" : [0]})
    df.to_csv(m2_bank_saving, index=False)


    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "BA", "BLK", "BMY"]})
    df.to_csv(m1_selection_df_path, index=False)


def test2():
    print("TESTING special case #1")
    df = pd.DataFrame({})
    df.to_csv(m2_stocks_2_shares_df_path, index=False)

    df = pd.DataFrame({ "Nasdaq_code" : ["SOLD_ALL"]})
    df.to_csv(m2_selection_df_path, index=False)

    df = pd.DataFrame({"bank_saving" : [888888]})
    df.to_csv(m2_bank_saving, index=False)


    df = pd.DataFrame({ "Nasdaq_code" : ["BA", "BLK", "BMY"]})
    df.to_csv(m1_selection_df_path, index=False)


def test3():
    print("TESTING special case #2")
    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"], 
                       "shares" : [1, 2, 3]})
    df.to_csv(m2_stocks_2_shares_df_path, index=False)

    df = pd.DataFrame({ "Nasdaq_code" : ["ASML", "AMD", "ABT"]})
    df.to_csv(m2_selection_df_path, index=False)

    df = pd.DataFrame({"bank_saving" : [0]})
    df.to_csv(m2_bank_saving, index=False)


    df = pd.DataFrame({ "Nasdaq_code" : ["SOLD_ALL"]})
    df.to_csv(m1_selection_df_path, index=False)




def test4():
    print("TESTING special case #3")
    df = pd.DataFrame({})
    df.to_csv(m2_stocks_2_shares_df_path, index=False)

    df = pd.DataFrame({ "Nasdaq_code" : ["SOLD_ALL"]})
    df.to_csv(m2_selection_df_path, index=False)

    df = pd.DataFrame({"bank_saving" : [888888]})
    df.to_csv(m2_bank_saving, index=False)


    df = pd.DataFrame({ "Nasdaq_code" : ["SOLD_ALL"]})
    df.to_csv(m1_selection_df_path, index=False)



    
