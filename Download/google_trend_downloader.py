
###########
# Doc:
#
###########


from Download.feature_downloader_template import feature_downloader_template
from Utils.google_trends_utils import get_dataset_google_trend_score_for_keyword
from Utils.google_trend_scoring_strategy import compute_google_trend_score_for_keyword_from_dataset
import pandas as pd
import csv



class google_trend_downloader(feature_downloader_template):
    default_download_func = get_dataset_google_trend_score_for_keyword
    default_process_func = compute_google_trend_score_for_keyword_from_dataset
    name = "google_trend"


    # NASDAQ_Code is needed for download_func to write log
    # keyword is searched for google trend
    # Start date is the earliest date to search for google trends
    def __init__(self, NASDAQ_code, keyword, 
                start_date = "2018-02-18",
                download_func=None,
                process_func=None
                ):

        if download_func is None:
            download_func = google_trend_downloader.default_download_func
        if process_func is None:
            process_func = google_trend_downloader.default_process_func

        work_dir = "Data/Feature/" + NASDAQ_code + "/" + "Raw_Features/Google_Trends/" + keyword

        #Using the super class to ensure a standard enviroment of instantiation
        super().__init__(NASDAQ_code, keyword, start_date, download_func, process_func, work_dir)

    def sanity_check_if_keyword_has_data_on_default_start_date():
        return google_trend_downloader.default_download_func


    
    def type_of_feature_downloader(self):
        return google_trend_downloader.name

    
    # write downloaded feature to disk, aka, creating a file
    # since the data downloaded is df, we can just use df.to_csv
    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raw_feature.to_csv(self.work_dir + "/" + file_name)




    # process the raw data correspondes to date
    # and create its corresponding counter parts in /Processed_Feature/
    def store_processed_feature_to_Data(self, date):
        path_to_raw_feature = self.work_dir + "/" + date + ".csv"
        df = pd.read_csv(path_to_raw_feature)
        score_vector_df = self.process_func(df, self.keyword)
        path_to_processed_table = self.process_work_dir + "/" + date +".csv"
        score_vector_df.to_csv(path_to_processed_table)

        


