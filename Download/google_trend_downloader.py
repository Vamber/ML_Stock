

from Download.feature_downloader_interface import feature_downloader_interface
from Utils.google_trends_utils import get_dataset_google_trend_score_for_keyword
from Utils.google_trend_scoring_strategy import compute_google_trend_score_for_keyword_from_dataset

import os
from os import path
import csv
import pandas as pd

class google_trend_downloader(feature_downloader_interface):



    # NASDAQ_Code is needed for download_func to write log
    # keyword is searched for google trend
    # Start date is the earliest date to search for google trends
    def __init__(self, NASDAQ_code, keyword, 
                start_date = "2018-2-18",
                download_func=get_dataset_google_trend_score_for_keyword,
                process_func=compute_google_trend_score_for_keyword_from_dataset
                ):

        #initilize all instance variable value
        self.NASDAQ_code = NASDAQ_code
        self.keyword = keyword
        self.start_date = "2018-2-18"
        self.download_func = download_func
        self.process_func = process_func

        # setting up path to work_dir
        # A work_dir, in a sense, is where the downloader function does its work
        # For example, it contains all downloaded raw features, dates_downloaded.csv, dates_not_downloaded.csv,
        # last_date_process.csv

        self.work_dir = "Data/Feature/" + self.NASDAQ_code + "/" + "Raw_Features/Google_Trends/" + self.keyword

        if not path.exists(self.work_dir):
            os.makedirs(self.work_dir)

        # create dates_downloaded.csv, dates_not_downloaded.csv, last_date_process.csv, if not exist
        # and write the collumn header in them

        for file_name in ["dates_downloaded.csv" , "dates_not_downloaded.csv",  "last_date_processed.csv"]:
            file_name = self.work_dir + "/" + file_name
            if not path.exists(file_name):
                with open(file_name, mode = "w") as f:
                    f = csv.writer(f)
                    f.writerow(["dates"])

    








    def check_date_for_latest_download(self):
        dates_downloaded_table_path = self.work_dir + "/" + "dates_downloaded.csv"
        
        df = pd.read_csv(dates_downloaded_table_path)
        if df.empty:
            return self.start_date
        else:
            #inherited from Super
            df = self.sort_table_by_dates(dates_downloaded_table_path)
            return df.iloc[-1]["dates"]


    def f(self):
        return self.get_lst_of_dates_between_target_and_yesterday("2021-2-18")

                


