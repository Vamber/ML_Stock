


from datetime import date
import pandas as pd
import numpy as np
from os import path
import os


class expert_template():

    def __init__(self, expert_name):
        self.ROOT = "/home/vamber/ML_stock/"
        self.name = expert_name
        self.work_dir = self.ROOT + "/Data/Expert/" + self.name
        self.daily_dir = self.work_dir + "/daily_choice/"
        # 100 k boi
        self.starting_wealth = 100000

        if not path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        if not path.exists(self.daily_dir):
            os.makedirs(self.daily_dir)
        
        #also init the wealth table if it doesn't exist, means the experting is only put into use today 
        wealth_df_path = self.work_dir + "/" + "wealth.csv"
        if not path.exists(wealth_df_path):

            df = pd.DataFrame({"date" : [self.get_recent_2_week_days(str(date.today()))[0]],
                                "wealth" :  [self.starting_wealth]})
            df.to_csv(wealth_df_path, index=False)

    
    ##
    ##
    def create_today_stock_selection(self):
        raise Exception ("CRITCAL, create_today_stock_selection not implemented in child class")


    #this function also reindex by Nasdaq_code for later uses's convinience 
    def get_5_dfs_from_ml_model(self):
        today = str(date.today())
        path_to_df_dir = self.ROOT + "/Data/ML_Models/Daily_Prediction/" + today + "/"
        lst_of_the_5_df = []
        lst_of_df_names = ["prediction.csv", "hist_acc_df.csv", "hist_recall_df.csv", "last_10d_acc_df.csv", "last_10d_recall_df.csv"]
        for df_name in lst_of_df_names:
            df = pd.read_csv(path_to_df_dir + df_name)
            df = df.set_index("Nasdaq_code")
            lst_of_the_5_df.append( df )

        return lst_of_the_5_df


    def save_today_stock_selection(self, selection_lst):
        today = str(date.today())
        today_dir = self.daily_dir + "/" + today + "/"
        if not path.exists(today_dir):
            os.makedirs(today_dir)

        df = pd.DataFrame({"Nasdaq_code" : selection_lst})
        df.to_csv( today_dir + "/stock_selection_lst.csv", index=False)

    



    # so this function is a little hard to wrap your head around
    # suppose today is 01-16
    # and the stock you own on 01-14 is (A, B, C, D) each with share (Ka, Kb, Kc, Kd)
    # and the stock you decided to buy on 01-15 are (A, J, V), and at this point (the share is actually unknown)
    # task 1: calculate how many shares of each stock actually was bought yesterday on 01-15
    # the first step is to calc the money obtained by selling, B, C, D on the opening price of of 01-15 (we don't sell A since A is already in the portfolio)
    # Let's call the total money obtained by selling TOTAL, 
    # the next step to calculate Kj, Kv by distributing TOTAL evenly across J and V by examinating J and V's opening price on Jan 01-15
    # then save (Ka, Kj, Kv) into a file
    # now calculate the total wealth by examinating closing price of A, J, V and that is the total price
    # then save the total wealth
    # special case: 
    #         "SELL_ALL" indicates we want to sell all stocks on a given day 
    #          case 1: we "SELL_ALL" on 01-14, but buy (A, B, C) on 01-15
    #                  in this case, there must be a existing file called bank_saving/01-14, and it stores a number which is obtained by selling all stocks at the opening price of 01-14
    #                  importantly, we don't care which stocks were sold to get that wealth, the number must exist
    #
    #
    #                  then we take that Money, and devide evenly across A, B, C to get Ka, Kb, Kc, and just save+compute wealth
    #
    #          case_2: stock (W E R) were purchase on 01-14, but we "SELL_ALL" on 01-15
    #                   in the case, we simply sell (W E R) at the opening price of 01-15, and save this as bank_saving/01-15, and just return this TOTAL as the compute wealth
    #
    #
    #          case_3: we "SELL_ALL" on 01-14 and "SELL_ALL" on 01-15. This is the easist case,
    #                   simpply read banking_saving/01-14  and   save this as banking_saving/01-15     
    #
    #
    #
    #
    #          case_4: the expert forgot to predict on weekdays (maybe I turned it off for some reason), 
    #                   #then I really don't want to code all different case again, just grab the most recently wealth possible
    #                   #either 01-14 or 01-15 is missing, just trieve the most recent wealth, and setting 01-15 as SOLD_ALL
    #                   #and saving this msg into log
    #  
    #
    #
    # I will code all cases in the following function sequentially for readability (I know there is room for optimization)
    #
    #
    #

    def simulate_wealth(self):
        self.simulate_wealth_helper(str(date.today()))

        
    def simulate_wealth_helper(self, date):
        
        day_m1, day_m2 = self.get_recent_2_week_days(date)
        print(day_m1, day_m2)

        

        ##
        ## handling the case when the model was just initialized or there is data missing somehow
        if self.dir_missing_for_date(day_m1) or self.dir_missing_for_date(day_m2):
            money = self.get_most_recent_wealth()
            if self.dir_missing_for_date(day_m1):
                os.makedirs(self.daily_dir + "/" + day_m1)
            df = pd.DataFrame({ "Nasdaq_code" : ["SOLD_ALL"]})
            df.to_csv(self.daily_dir + "/" + day_m1 + "/" + "stock_selection_lst.csv", index=False)
            self.save_3_data_for_wealth_sim({}, money, day_m1)
            return

    
        # general_case: 
        if not self.sold_all_stocks_on_date(day_m2) and not self.sold_all_stocks_on_date(day_m1):
            #
            stock_2_shares_day_m2 = self.get_stock_2_shares_on_date(day_m2)
            #print(stock_2_shares_day_m2)
            #
            stock_selection_day_m1 = self.get_stock_selection_on_date(day_m1)
            #print(stock_selection_day_m1)
            #
            stocks_2_shares_sold_on_day_m1 = {}
            stock_2_shares_hold_on_day_m1 = {}
            #
            
            
            for Nasdaq_code, shares in stock_2_shares_day_m2.items():
                if Nasdaq_code not in stock_selection_day_m1:
                    stocks_2_shares_sold_on_day_m1[Nasdaq_code] = shares
                else:
                    stock_2_shares_hold_on_day_m1[Nasdaq_code] =  shares

            #print(stocks_2_shares_sold_on_day_m1)
            #print(stock_2_shares_hold_on_day_m1)       
            #
            money = self.compute_money_after_selling_stock_selection_on_date(stocks_2_shares_sold_on_day_m1, day_m1)
            #print(money)
            #
            stocks_to_buy_on_day_m1 = [s for s in stock_selection_day_m1 if s not in stock_2_shares_hold_on_day_m1] 
            #print(stocks_to_buy_on_day_m1)
            stock_2_shares_after_buying_on_day_m1 = self.compute_stock_2_shares_map_with_money_on_date(stocks_to_buy_on_day_m1, day_m1, money)
            #print(stock_2_shares_after_buying_on_day_m1)
            # including the unsold stock
            stock_2_shares_after_buying_on_day_m1.update(stock_2_shares_hold_on_day_m1)
            #print(stock_2_shares_after_buying_on_day_m1)
            #
            #
            self.save_3_data_for_wealth_sim(stock_2_shares_after_buying_on_day_m1, 0, day_m1)
            wealth_df = pd.read_csv(self.work_dir + "/wealth.csv")
            


        # special case 1
        elif self.sold_all_stocks_on_date(day_m2) and not self.sold_all_stocks_on_date(day_m1):
            money = self.get_bank_saving_on_date(day_m2)
            #print(money)
            stock_selection_day_m1 = self.get_stock_selection_on_date(day_m1)
            stock_2_shares_after_buying_on_day_m1 = self.compute_stock_2_shares_map_with_money_on_date(stock_selection_day_m1, day_m1, money)
            #print(stock_2_shares_after_buying_on_day_m1)
            self.save_3_data_for_wealth_sim(stock_2_shares_after_buying_on_day_m1, 0, day_m1)

        # special case 2
        elif not self.sold_all_stocks_on_date(day_m2) and self.sold_all_stocks_on_date(day_m1):
            stock_2_shares_day_m2 = self.get_stock_2_shares_on_date(day_m2)
            money = self.compute_money_after_selling_stock_selection_on_date(stock_2_shares_day_m2, day_m1)
            #print(money)
            self.save_3_data_for_wealth_sim({}, money, day_m1)

        # special case 3
        elif self.sold_all_stocks_on_date(day_m2) and self.sold_all_stocks_on_date(day_m1):
            money = self.get_bank_saving_on_date(day_m2)
            self.save_3_data_for_wealth_sim({}, money, day_m1)











            





    # helper 1
    def get_stock_opening_price_on_date(self, Nasdaq_code, date):
        df = pd.read_csv(self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Stock_Price/price.csv")
        return df[df["Date"] == date]["Open"].iloc[0]

    # helper 2
    def get_stock_closing_price_on_date(self, Nasdaq_code, date):
        df = pd.read_csv(self.ROOT + "/Data/Feature/" + Nasdaq_code + "/Processed_Features/Stock_Price/price.csv")
        return df[df["Date"] == date]["Close"].iloc[0]

    # helper 3
    def compute_money_after_selling_stock_selection_on_date(self, stock_2_shares_map, date):
        total_money = 0
        for Nasdaq_code, shares_holding in stock_2_shares_map.items():
            total_money += self.get_stock_opening_price_on_date(Nasdaq_code, date) * stock_2_shares_map[Nasdaq_code]
        return total_money

    # helper 3.5 
    def compute_wealth_of_stock_2_shares_after_closing_on_date(self, stock_2_shares_map, date):
        total_money = 0
        for Nasdaq_code, shares_holding in stock_2_shares_map.items():
            total_money += self.get_stock_closing_price_on_date(Nasdaq_code, date) * stock_2_shares_map[Nasdaq_code]
        return total_money


    # helper 4
    def compute_stock_2_shares_map_with_money_on_date(self, stock_selection_lst, date, money):
        stock_2_opening_price_map = {}
        for Nasdaq_code in stock_selection_lst:
            stock_2_opening_price_map[Nasdaq_code] = self.get_stock_opening_price_on_date(Nasdaq_code, date)
    
        num_stocks = len(stock_selection_lst)
        #target_val means each stock is suppose to hold this much value in dollar
        target_val = money/num_stocks
        #
        stock_2_shares_map = {}
        for Nasdaq_code, opening_price in stock_2_opening_price_map.items():
            stock_2_shares_map[Nasdaq_code] = target_val / opening_price
    
        return stock_2_shares_map

    # helper 5
    def get_yesterday(self, date):
        return str(pd.Timestamp(date) - pd.Timedelta(1)).split(' ')[0]


    # helper 6
    def get_recent_2_week_days(self, date):
    
        def get_recent_1_week_day(date):
            yesterday = self.get_yesterday(date)
            if pd.Timestamp(yesterday).dayofweek > 4:
                return get_recent_1_week_day(yesterday)
            return yesterday

        days = []
        day_1 = get_recent_1_week_day(date)
        day_2 = get_recent_1_week_day(day_1)
        days.append(day_1)
        days.append(day_2)
        #
        return days

    # helper 7
    # 
    def save_3_data_for_wealth_sim(self, stock_2_shares_map, bank_saving, day_m1):

        #
        if len(stock_2_shares_map) == 0:
            wealth = bank_saving
        else:
            wealth = self.compute_wealth_of_stock_2_shares_after_closing_on_date(stock_2_shares_map, day_m1)
        #
        wealth_df = pd.read_csv(self.work_dir + "/wealth.csv")
        wealth_df.loc[len(wealth_df)] = [day_m1, wealth]
        wealth_df.to_csv(self.work_dir + "/wealth.csv", index=False)
        #
        stock_2_shares_df = pd.DataFrame({"Nasdaq_code": list(stock_2_shares_map.keys()) ,
                                              "shares" : list(stock_2_shares_map.values())})
        stock_2_shares_df.to_csv(self.daily_dir + "/" + day_m1 + "/stock_2_shares.csv", index=False)
        #
        bank_saving_df = pd.DataFrame({"bank_saving" : [bank_saving]})
        bank_saving_df.to_csv(self.daily_dir + "/" + day_m1 + "/bank_saving.csv", index=False)
        #
        print(wealth_df)



    #helper a1
    def get_stock_2_shares_on_date(self, date):
        df_path = self.daily_dir + "/" + date + "/" + "stock_2_shares.csv"
        df = pd.read_csv(df_path)
        stock_2_shares_map = {}
        nasdaq_lst = list(df["Nasdaq_code"])
        shares_lst = list(df["shares"])
        for i in range(0, len(nasdaq_lst)):
            nasdaq = nasdaq_lst[i]
            shares = shares_lst[i]
            stock_2_shares_map[nasdaq] = shares
        
        return stock_2_shares_map


    #helper a2
    def get_stock_selection_on_date(self, date):
        df_path = self.daily_dir + "/" + date + "/" + "stock_selection_lst.csv"
        df = pd.read_csv(df_path)
        return list(df["Nasdaq_code"])

    #helper a3
    def sold_all_stocks_on_date(self, date):
        l = self.get_stock_selection_on_date(date)
        return len(l) == 1 and l[0] == "SOLD_ALL"

    #helper a4
    def get_bank_saving_on_date(self, date):
        df_path = self.daily_dir + "/" + date + "/" + "bank_saving.csv"
        df = pd.read_csv(df_path)
        return list(df["bank_saving"])[0]

    #helper a5
    def dir_missing_for_date(self, date):
        date_dir = self.daily_dir + "/" + date
        return not path.exists(date_dir)

    #helper a6
    def get_most_recent_wealth(self):
        wealth_df = pd.read_csv(self.work_dir + "/wealth.csv")
        return list(wealth_df["wealth"])[-1]





    ##
    ##
    ## this is a helper function that doesn't must be by child class
    ##
    ## it iteratively filters out the selection from the 5dfs
    ##
    ## val_config_lst[0] = 1 or -1 for prediction
    ## val_config_lst[1] = min for hist_acc
    ## val_config_lst[2] = max for hist recall
    ## val_config_lst[3] = min for last 10d acc
    ## val_config_lst[4] = max for last 10d recall
    ##
    def get_nmp_after_iterative_filtering(self, val_config_lst):
        prediction_df, hist_acc_df, hist_recall_df, last_10d_acc_df, last_10d_recall_df = self.get_5_dfs_from_ml_model()
        unfiltered_nmp_lst = self.init_unfiltered_nmp_lst(prediction_df)
        nmp_lst_with_pred_1 = self.filter_nmp_from_df_base_on_condition(prediction_df, "_pred", unfiltered_nmp_lst, lambda x: x==val_config_lst[0])
        nmp_lst_with_good_hist_acc = self.filter_nmp_from_df_base_on_condition(hist_acc_df, "_hist_acc", nmp_lst_with_pred_1, lambda x: x>= val_config_lst[1])
        nmp_lst_with_good_hist_recall = self.filter_nmp_from_df_base_on_condition(hist_recall_df, "_hist_recall", nmp_lst_with_good_hist_acc, lambda x: x <= val_config_lst[2])
        nmp_lst_with_good_last_10d_acc = self.filter_nmp_from_df_base_on_condition(last_10d_acc_df, "_last_10d_acc", nmp_lst_with_good_hist_recall, lambda x : x>= val_config_lst[3])
        nmp_lst_with_good_last_10d_recall = self.filter_nmp_from_df_base_on_condition(last_10d_recall_df, "_last_10d_recall", nmp_lst_with_good_last_10d_acc, lambda x : x<= val_config_lst[4])


        return nmp_lst_with_good_last_10d_recall




    

    ##
    ## helper 1
    def init_unfiltered_nmp_lst(self, prediction_df):
        lst_of_nasdaq = list(prediction_df.index)
        lst_of_model = [j.replace("_pred", "") for j in [c for c in prediction_df if "_pred" in c]]
        # A full cross product of the 
        unfiltered_nmp_lst = [(nasdaq, model) for nasdaq in lst_of_nasdaq for model in lst_of_model ]
        return unfiltered_nmp_lst

    
    ##
    ## helper 2
    def filter_nmp_from_df_base_on_condition(self, df, df_type, cur_nmp_lst, cond_func):
    
        filtered_nmp_lst = []
        for nmp in cur_nmp_lst:
            nasdaq_code = nmp[0]
            model = nmp[1]
            val = df.loc[nasdaq_code, model + df_type]
            if cond_func(val):
                filtered_nmp_lst.append((nasdaq_code, model))

        return filtered_nmp_lst

    

    #checks if yesterday the market was dropping
    def market_dropped_yesterday(self):

        #sorry for the horrible reuse of function here
        #code starts to get ugly at this point 
        #does Linlin want to fix this for me ?
        def get_recent_1_week_day(date):
            yesterday = self.get_yesterday(date)
            if pd.Timestamp(yesterday).dayofweek > 4:
                return get_recent_1_week_day(yesterday)
            return yesterday

        path_to_IXIC = self.ROOT + '/Data/Feature/^IXIC/Processed_Features/Stock_Price/price.csv'
        df = pd.read_csv(path_to_IXIC)

        today = str(date.today())
        prev_date = get_recent_1_week_day(today)

        # get previous market opening day
        df = df[df["Date"] == prev_date]

        open_price = df["Open"].iloc[0]
        close_price = df["Close"].iloc[0]

        #more readable
        if close_price / open_price < 1:
            return True
        else:
            return False




    
