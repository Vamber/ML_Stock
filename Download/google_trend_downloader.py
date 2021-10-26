

from Download.feature_downloader_template import feature_downloader_template
from Utils.google_trends_utils import get_dataset_google_trend_score_for_keyword
from Utils.google_trend_scoring_strategy import compute_google_trend_score_for_keyword_from_dataset





class google_trend_downloader(feature_downloader_template):



    # NASDAQ_Code is needed for download_func to write log
    # keyword is searched for google trend
    # Start date is the earliest date to search for google trends
    def __init__(self, NASDAQ_code, keyword, 
                start_date = "2018-2-18",
                download_func=get_dataset_google_trend_score_for_keyword,
                process_func=compute_google_trend_score_for_keyword_from_dataset
                ):

      

        work_dir = "Data/Feature/" + NASDAQ_code + "/" + "Raw_Features/Google_Trends/" + keyword

        #Using the super class to ensure a standard enviroment of instantiation
        super().__init__(NASDAQ_code, keyword, start_date, download_func, process_func, work_dir)

    


    
    # write downloaded feature to disk, aka, creating a file
    # since the data downloaded is df, we can just use df.to_csv
    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raw_feature.to_csv(self.work_dir + "/" + file_name)



        


