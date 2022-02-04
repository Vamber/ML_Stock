


##############
#
# According to the design of this module, every feature needs to have its corresponding 
# feature_downloader_object, for example, google trends, needs to have a google_trends_downloader_object
#
# Every feature downloader must inherit from feature_downloader_interface
# And rewrite every method implemented 
#
##############

import pandas as pd 
from datetime import date
from datetime import timedelta
import csv
from os import path
import os
import datetime as DT
import concurrent.futures 

class feature_downloader_template():


    # every subclass must call super.()__init__ to ensure standard sets of instance variable
    def __init__(self, NASDAQ_code, keyword,  start_date,
                download_func,  process_func,  work_dir
                ):

        self.NASDAQ_code = NASDAQ_code
        self.keyword = keyword
        self.start_date = start_date
        self.download_func = download_func
        self.process_func = process_func
        self.work_dir = work_dir
        self.processed_work_dir = self.work_dir.replace("/Raw_Features/", "/Processed_Features/")

        if not path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        if not path.exists(self.processed_work_dir):
            os.makedirs(self.processed_work_dir)

        for file_name in ["dates_downloaded.csv" , "dates_not_downloaded.csv",  "dates_processed.csv"]:
            file_name = self.work_dir + "/" + file_name
            if not path.exists(file_name):
                with open(file_name, mode = "w") as f:
                    f = csv.writer(f)
                    f.writerow(["dates"])
  


    ##
    # @Need to be Over-Write
    ##

    ##
    # This function is important, because it will be used by gnerate_stock_features_csv.py
    # For example if I want the google trend for the keyword RTX 3090 on day 2018-2-18
    # But RTX 3090 was not even out yet, there will just be no data on 2018-2-18
    # This means I can't have 3090 as a feature if default date is 2018-2-18
    # 
    ## 

    def sanity_check_if_keyword_has_data_on_default_start_date():
        raise Exception("sanity_check_if_keyword_has_data_on_default_start_date " + "not implemented")


    ##
    # @Need to be Over-Write
    ##
    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raise Exception("store_raw_feature_to_Data" + "not implemented")

    #####
    #@Need to be Overwrite by child class
    #
    ####
    def store_processed_feature_to_Data(self, date):
        raise Exception("store_processes_feature_to_Data" + " not implemented")

    #####
    # @ Need to be Over_write
    #
    ######
    def type_of_feature_downloader(self):
        raise Exception("type_of_feature_downloader" + "not implemented")

    




    def describe(self):
        s =  "[" + self.type_of_feature_downloader() + "]" + "  " 
        s += "[" + self.NASDAQ_code + "]" + "  "
        
        # stock price really doesn't have a keyword
        if not self.type_of_feature_downloader() == "stock_price":
            s += "[" + self.keyword + "]" + " "

        s += self.check_date_for_latest_download() + " "
        s += "Download_success=" + str(self.is_download_successful_for_everyday()) + " "
        s += "Process_raw_feature_success="  + str(self.is_processing_raw_feature_successful_for_everyday())
        return s




    #core
    def download_raw_feature_data_for_just_one_day(self, date):
        
        success = ""

        data = self.download_func(self.NASDAQ_code, date, self.keyword)

        if data is None:
            self.append_date_to_dates_not_downloaded_csv(date)

        else:
            self.append_date_to_dates_downloaded_csv(date)
            self.store_raw_feature_to_Data(data, date + ".csv")
            success = "$"

        s = self.keyword
        s = s + (30-len(s))*" " + date
        print(s + (45-len(s))*" " + success)


    #core
    #For Lazy redownload case
    #giving up downloading for google trend if the date is between 2021-08-08->2021-10-03
    def download_raw_feature_data_for_just_one_day_LAZY(self, date):

        if self.type_of_feature_downloader() == "google_trend" and date >= "2021-08-08" and date <= "2021-10-03":
            #skipping attemp to download
            print("Google-trend-missing date domain, skipped   " + date)
            self.append_date_to_dates_not_downloaded_csv(date)
            return
        
        else:
            self.download_raw_feature_data_for_just_one_day(date)
    
        

    #core
    # Download the raw feature for every single between last download and today
    # 
    def download_raw_feature_data(self):
        last_downloaded_date = self.check_date_for_latest_download()
        lst_of_dates = self.get_lst_of_dates_between_target_and_yesterday(last_downloaded_date)

        # downloading data concurrenly
        # the executor will automatically handle process scheudling 
        with concurrent.futures.ThreadPoolExecutor(max_workers=48) as executor:
            executor.map(self.download_raw_feature_data_for_just_one_day, lst_of_dates)

        #since the downloading those dates might not be scheduled sequentially
        #we sort the table again
        #it's not exactly for function purpose, because check_last_downloaded_date will sort it again
        #it's just easier to read



    def redownload_missing_raw_feature_data(self):
        lst_of_dates = self.get_lst_of_dates_missing_and_clear_dates_not_downloaded()

        #Contemporary Complexity Requires Concurrency
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.download_raw_feature_data_for_just_one_day, lst_of_dates)

    #In this mode, all missing data between 2021-08-09 -> 2021-10-03 will be skipped
    def redownload_missing_raw_feature_data_lazy_mode(self):
        return 0


        

    
    ######
    ######
    # this section creates the Multiprocess code for the above two function
    # allow them to be multiprocessed from Hypervisor's perspective
    # essential the function returns a list of process, but actually don't execute them
    # whereas the hypervisor paralles them 

    #core
    def make_proc(self, date):
        return lambda : self.download_raw_feature_data_for_just_one_day(date)

    #core
    #for Lazy Redownload feature
    def make_proc_LAZY(self, date):
        return lambda : self.download_raw_feature_data_for_just_one_day_LAZY(date)

    #core
    def download_raw_feature_data_get_lst_of_process(self):
        #proc_lst contains bunch of lambad functions takes in no args, each one of them performs download for one day
        proc_lst = []
        last_downloaded_date = self.check_date_for_latest_download()
        lst_of_dates = self.get_lst_of_dates_between_target_and_yesterday(last_downloaded_date)
        for date in lst_of_dates:
            proc_lst.append(self.make_proc(date))

        return proc_lst

    #core
    def redownload_missing_raw_feature_data_get_lst_of_process(self):
        proc_lst = []
        lst_of_dates = self.get_lst_of_dates_missing_and_clear_dates_not_downloaded()
        for date in lst_of_dates:
            proc_lst.append(self.make_proc(date))

        return proc_lst

    #core
    #download all the missing datas, but skip if the date is between "2021-08-09 -->2021-10-03 for google trend"
    def redownload_missing_raw_feature_data_get_lst_of_process_LAZY(self):
        proc_lst = []
        lst_of_dates = self.get_lst_of_dates_missing_and_clear_dates_not_downloaded()
        for date in lst_of_dates:
            proc_lst.append(self.make_proc_LAZY(date))

        return proc_lst






    # core
    # basically if there is any day not downloaded, return false
    # only when the dates_not_downloaded.csv is empty, return True
    def is_download_successful_for_everyday(self):
        missing_data_table_path = self.work_dir + "/" + "dates_not_downloaded.csv"
        df = pd.read_csv(missing_data_table_path)
        return df.empty



    #core
    #clever way to check if processing is good
    def is_processing_raw_feature_successful_for_everyday(self):
        return len(self.get_lst_of_dates_downloaded()) == len(self.get_lst_of_dates_processed()) 

    



    ###
    ### Let A be the set of dates of raw_features downloaded
    ### Let B be the set of dates of features processed
    ### 
    ### It is clear that B is a subset of A
    ### 
    ### Find B Union ^A, and process them all
    ###
    ###

    #core
    def process_raw_feature(self):

       
        lst_of_dates = self.get_lst_of_dates_downloaded_but_not_processed()

        for date in lst_of_dates:
            self.store_processed_feature_to_Data(date)
            print(self.keyword + (30-len(self.keyword)) * " " + date)

        for date in lst_of_dates:
            self.append_date_to_dates_processed_csv(date)

    













































    ##############
    #
    # All the sections below deals with dates related stuffs
    # Such as dates checking, and writting to dates
    #
    ##############






    #this helper function can be inherited 
    def check_date_for_latest_download(self):
        dates_downloaded_table_path = self.work_dir + "/" + "dates_downloaded.csv"
        
        df = pd.read_csv(dates_downloaded_table_path)
        if df.empty:
            return self.start_date
        else:
            #inherited from Super
            df = self.sort_table_by_dates(dates_downloaded_table_path)
            return df.iloc[-1]["dates"]

    


    #helper
    def get_lst_of_dates_missing_and_clear_dates_not_downloaded(self):
        missing_dates_table_path = self.work_dir + "/" + "dates_not_downloaded.csv"
        df = pd.read_csv(missing_dates_table_path)

        os.remove(missing_dates_table_path)
        with open(missing_dates_table_path, mode = "w") as f:
            f = csv.writer(f)
            f.writerow(["dates"])

        #notice how there is a unique() there,
        #this was implemented this way because there could be redundant dates
        
        return list(df["dates"].unique())


    #helper
    def clear_dates_processed(self):
        df_path = self.work_dir + "/" + "dates_processed.csv"
        os.remove(df_path)
        with open(mdf_path, mode = "w") as f:
            f = csv.writer(f)
            f.writerow(["dates"])


    #helper
    #sort the table, and also update the file-system
    def sort_table_by_dates(self, path_to_table):
        df = pd.read_csv(path_to_table)
        df = df.sort_values(by="dates", ascending = True)
        os.remove(path_to_table)
        df.to_csv(path_to_table, index=False)
        return df

    #helper
    def get_lst_of_dates_downloaded(self):
        path_to_table = self.work_dir + "/" + "dates_downloaded.csv"
        df = pd.read_csv(path_to_table)
        return list(df["dates"])


    #helper
    def get_lst_of_dates_not_downloaded(self):
        path_to_table = self.work_dir + "/" + "dates_not_downloaded.csv"
        df = pd.read_csv(path_to_table)
        return list(df["dates"])


    #helper
    def get_lst_of_dates_processed(self):
        path_to_table = self.work_dir + "/" + "dates_processed.csv"
        df = pd.read_csv(path_to_table)
        return list(df["dates"])
        
    #helper
    def get_lst_of_dates_downloaded_but_not_processed(self):
        lst_dates_downloaded = self.get_lst_of_dates_downloaded()
        lst_dates_processed  = self.get_lst_of_dates_processed()
        return list(set(lst_dates_downloaded) - set(lst_dates_processed))
    
    
    #helper
    # The purpose of this function is more for checking which dates are missing easily
    # For example, currenly, it seems like all the google trend data are simply just missing between 2021-8-10 -->2021-10-15, and no one knows why
    def get_lst_of_missing_dates_time_sections(self):

        if self.is_download_successful_for_everyday():
            return []


        missing_dates = self.get_lst_of_dates_not_downloaded()
        missing_dates.sort()
        
        prev_date_obj = DT.date(2000, 2, 14)
        missing_dates_time_sections = []

        for cur_date in missing_dates:
            cur_date_obj = self.date_str_2_date_obj(cur_date)
            if cur_date_obj - DT.timedelta(days=1) != prev_date_obj:
                missing_dates_time_sections.append(str(prev_date_obj) + "<-")
                missing_dates_time_sections.append(cur_date + "->")
            prev_date_obj = cur_date_obj

        missing_dates_time_sections.append(cur_date + "<-")
        return missing_dates_time_sections


#turn a date in string format, "2020-08-15" --> Date(2020,08,15)
    def date_str_2_date_obj(self, date_str):
        year_month_day_lst = date_str.split("-")
        year = int(year_month_day_lst[0])
        month = int(year_month_day_lst[1])
        day = int(year_month_day_lst[2])
        date_obj = DT.date(year, month, day)
        return date_obj



    # return a lst looking like this ["2019-1-11", "209-1-12" ... "yesterday"]
    def get_lst_of_dates_between_target_and_yesterday(self, target_date):

        yesterday = str(date.today() - timedelta(days = 1))
        target_date = self.date_str_2_date_obj(target_date)
        target_date = target_date+ DT.timedelta(days=1)

        #if the target date is 2018-2-18, then we would want to start downloading on
        #    2018-2-19, because the data from 2018-2-18 has already been downloaded. 
        dates = list(pd.date_range(start = target_date, end = yesterday))    
        return [str(i).split()[0] for i in dates]


    
    def get_lst_of_dates_between_two_date(self, from_date, to_date):
        from_date = self.date_str_2_date_obj(from_date)
        from_date = from_date + DT.timedelta(days=1)

        dates = list(pd.date_range(start = from_date, end = to_date))    
        return [str(i).split()[0] for i in dates]



    def append_date_to_dates_downloaded_csv(self, date):
        path_to_table = self.work_dir + "/" + "dates_downloaded.csv"
        with open(path_to_table, mode = "a") as f:
            f = csv.writer(f)
            f.writerow([date])
    
    def append_date_to_dates_not_downloaded_csv(self, date):
        path_to_table = self.work_dir + "/" + "dates_not_downloaded.csv"
        with open(path_to_table, mode = "a") as f:
            f = csv.writer(f)
            f.writerow([date])

    def append_date_to_dates_processed_csv(self, date):
        path_to_table = self.work_dir + "/" + "dates_processed.csv"
        with open(path_to_table, mode = "a") as f:
            f = csv.writer(f)
            f.writerow([date])

    #when dates_not_downloaded.csv is corruptted, this is the function to call 
    #it computes date not downloaded based on date downloaded
    def dates_missing_data_corruption_recovery(self):
        
        if self.type_of_feature_downloader() == "stock_price":
            return

        last_downloaded_date = self.check_date_for_latest_download()
        default_start_date = self.start_date
        lst_of_dates_need_to_be_downloaded = self.get_lst_of_dates_between_two_date(default_start_date, last_downloaded_date)
        dates_downloaded = self.get_lst_of_dates_downloaded()

        #clean dates downloaded table, since it could be corrupted
        self.get_lst_of_dates_missing_and_clear_dates_not_downloaded()

        dates_missing = list(set(lst_of_dates_need_to_be_downloaded) - set(dates_downloaded))
        for date in dates_missing:
            self.append_date_to_dates_not_downloaded_csv(date)


        


