


from Download.feature_downloader_template import feature_downloader_template
from Utils.stock_dataset_utils import get_historical_dataset_for_a_stock 
import pandas as pd
import csv
from datetime import date


class stock_price_downloader(feature_downloader_template):
    defualt_download_func = get_historical_dataset_for_a_stock
    default_process_func = lambda : 1/0
    name = "stock_price"
    data_df_name = "price.csv"

    # NASDAQ_Code is needed for download_func to write log
    # keyword is not needed for stock price
    # Start date is also not need for stock, since the API used will automatically download all data since
    # the first day first went to the market


    def __init__(self,
                NASDAQ_code, 
                keyword = "null", 
                start_date = "null",
                download_func=None,
                process_func=None   #still working on this
                ):

        if download_func is None:
            download_func = stock_price_downloader.defualt_download_func
        if process_func is None:
            process_func = stock_price_downloader.default_process_func

        work_dir = "Data/Feature/" + NASDAQ_code + "/" + "Raw_Features/Stock_Price" 

        #Using the super class to ensure a standard enviroment of instantiation
        super().__init__(NASDAQ_code, "null", "null", download_func, process_func, work_dir)

    
    def sanity_check_if_keyword_has_data_on_default_start_date():
        return stock_price_downloader.defualt_download_func


    def type_of_feature_downloader(self):
        return stock_price_downloader.name



    ##
    # The stock_price_downloader is intrinsically different from google_news and google_trend
    # Because you don't need to download the data from everyday like google_news or google_trend
    # 
    # once you call get_historical_dataset_for_a_stock, you literally get the opening price 
    # and the closing pricing price for every single day, so, there should only be one csv
    # containing stock price data
    #
    #
    # Therefore, it is important to overwrte download_raw_feature_data function
    #
    ## 
  
    def download_raw_feature_data(self):
        # notice how we are not looping through the dates at all
        
        today = str(date.today())
        data = self.download_func(self.NASDAQ_code)
        if data is None:
            self.append_date_to_dates_not_downloaded_csv(today)
        else:
            self.append_date_to_dates_downloaded_csv(today)
            self.store_raw_feature_to_Data(data, self.data_df_name)



    ########
    ## Like-wise, we need to over-write this function as well, however, it's a simple over-write
    ########
    def redownload_missing_raw_feature_data(self):

        today = str(date.today())
        #just using the method below to clear the datas_not_downloaded_csv
        #so that the behavior of is_download_successful_for_everyday is not effected
        self.get_lst_of_dates_missing_and_clear_dates_not_downloaded() 
        
        if self.check_date_for_latest_download() != today:
            self.download_raw_feature_data()

    


    #####
    # Like-wise, this function needs to be overloaded 
    #####
    def process_raw_feature(self):

        if not self.is_download_successful_for_everyday():
            return 
        
        last_date_processed = self.check_date_for_latest_process()
        last_date_downloaded = self.check_date_for_latest_download()
        #notice, the lst_of_dates actually doesn't include last_date_processed
        #Because it is already processes. 
        lst_of_dates = self.get_lst_of_dates_between_two_date(last_date_processed, last_date_downloaded)

        for date in lst_of_dates:
            self.store_processed_feature_to_Data(date)

        self.update_date_last_processed(last_date_downloaded)


    

    # write downloaded feature to disk, aka, creating a file
    # since the data downloaded is df, we can just use df.to_csv
    def store_raw_feature_to_Data(self, raw_feature, file_name):
        raw_feature.to_csv(self.work_dir + "/" + file_name)

    


    # process the raw data correspondes to date
    # and create its corresponding counter parts in /Processed_Feature/
    def store_processed_feature_to_Data(self, date):
        raise Exception("still working on this")