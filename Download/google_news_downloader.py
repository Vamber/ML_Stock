from Download.feature_downloader_template import feature_downloader_template
from Utils.google_news_utils import get_news_metadata_df_from_a_keyword_on_a_particular_date
import pandas as pd
import csv



class google_news_downloader(feature_downloader_template):

    default_download_func = get_news_metadata_df_from_a_keyword_on_a_particular_date
    default_process_func = lambda : 1/0
    name = "google_news"

    # NASDAQ_Code is needed for download_func to write log
    # keyword is searched for google news, and it must be contained within the news title
    # Start date is the earliest date to search for google trends
    def __init__(self, NASDAQ_code, keyword, 
                start_date = "2018-02-18",
                download_func=None,
                process_func=None
                ):

        if download_func is None:
            download_func = google_news_downloader.default_download_func
        if process_func is None:
            process_func = google_news_downloader.default_process_func

        

        work_dir = "Data/Feature/" + NASDAQ_code + "/" + "Raw_Features/Google_News/" + keyword

        #Using the super class to ensure a standard enviroment of instantiation
        super().__init__(NASDAQ_code, keyword, start_date, download_func, process_func, work_dir)



    def sanity_check_if_keyword_has_data_on_default_start_date():
        return google_news_downloader.default_download_func



    def type_of_feature_downloader(self):
        return google_news_downloader.name

    
    # write downloaded feature to disk, aka, creating a file
    # since the data downloaded is df, we can just use df.to_csv
    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raw_feature.to_csv(self.work_dir + "/" + file_name, index=False)




    # process the raw data correspondes to date
    # and create its corresponding counter parts in /Processed_Feature/
    def store_processed_feature_to_Data(self, date):
        raise Exception("This is not impletemented yet, Vamber is still thinking about this")