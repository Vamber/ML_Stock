


##############
#
# According to the design of this module, every feature needs to have its corresponding 
# feature_downloader_object, for example, google trends, needs to have a google_trends_downloader_object
#
# Every feature downloader must inherit from feature_downloader_interface
# And rewrite every method implemented 
#
##############

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




