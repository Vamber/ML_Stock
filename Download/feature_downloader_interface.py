


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

class feature_downloader_interface():

    def __init__(self):
        raise Exception("init method not implemented")


    def check_date_for_latest_download(self):
        raise Exception("check_date_for_latest_download not implemented")


    def download_raw_feature_data(self):
        raise Exception("download_raw_feature_data not implemented")


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




