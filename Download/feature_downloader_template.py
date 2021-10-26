


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

        if not path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        for file_name in ["dates_downloaded.csv" , "dates_not_downloaded.csv",  "last_date_processed.csv"]:
            file_name = self.work_dir + "/" + file_name
            if not path.exists(file_name):
                with open(file_name, mode = "w") as f:
                    f = csv.writer(f)
                    f.writerow(["dates"])
  





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



            


    # Download the raw feature for every single between last download and today
    # 
    def download_raw_feature_data(self):
        last_downloaded_date = self.check_date_for_latest_download()
        lst_of_dates = self.get_lst_of_dates_between_target_and_yesterday(last_downloaded_date)

        for date in lst_of_dates:
            data = self.download_func(self.NASDAQ_code, date, self.keyword)

            if data is None:
                self.append_date_to_dates_not_downloaded_csv(date)

            else:
                self.append_date_to_dates_downloaded_csv(date)
                self.store_raw_feature_to_Data(data, date + ".csv")




    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raise Exception("store_raw_feature_to_Data" + "not implemented")



    def get_lst_of_dates_missing_and_clear_dates_not_downloaded(self):
        raise Exception("get_lst_of_dates_missing_and_clear_dates_not_downloaded" + " not implemented")


    def redownload_missing_raw_feature_data(self):
        raise Exception("redownload_missing_raw_feature_data" + " not implemented")
    

    def is_download_successful_for_everyday(self):
        raise Exception("is_download_successful_for_everyday" + " not implemented")


    def process_raw_feature(self):
        raise Exception("process_raw_feature" + " not implemented")
    
    
    def reprocess_raw_feature(self):
        raise Exception("reprocess_raw_feature" + " not implemented")


    # despite this being an interface, there is still few method they can inherit
    # this method takes in a path to table with column called [dates], contains dates which may not be sorted
    # and return a df object, but with dates sorted in order
    # in the end, the original data_frame object on disk, is still unmodified
    # the design was implemented this way to reduce disk write. 
    def sort_table_by_dates(self, path_to_table):
        df = pd.read_csv(path_to_table)
        df = df.sort_values(by="dates", ascending = True)
        return df


    # return a lst looking like this ["2019-1-11", "209-1-12" ... "yesterday"]
    def get_lst_of_dates_between_target_and_yesterday(self, target_date):
        yesterday = str(date.today() - timedelta(days = 1))
        dates = list(pd.date_range(start = target_date, end = yesterday))    
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
        


