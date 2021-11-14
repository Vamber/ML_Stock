
from Download.google_trend_downloader import google_trend_downloader
from Download.google_news_downloader import google_news_downloader
from Download.stock_price_downloader import stock_price_downloader


# Purpose, aggreagre all feature_downloader into one large object called hypervisor
# For example, for NVDA, the feature "buy nvidia stock" can be a google trend feature,
# which means that this keyword would have it own downloader object
# however, one stock may have multiple features [NVDA] 
#                                               google_trend: "[buy nvidia stock, sell nvidia stock, nvidia stock]" 
#                                               google_news: "[Jensen Huang, Bitcoin, Etheruem]"
# the idea of a hypervisor to aggregate them togther, for better automation of downloading data, 
# for better monitoring of any missig data 
# 
# Each row in stock_and_features.csv form a bijection with its own stock_feature hypervisor 






###
# A classic layout of: 
# feature_downloader_type_to_kw_lst_Map = {
#          google_trend_downloader : ["buy Telsa stock", "sell Tesla stock", "Tesla stock",]
#          google_news_downloader : ["Elon Musk" , "Battery"]
#          stock_price_downloader : ["null"]  <--- for stock price downloader, kw must be null and also exactly one element, two elements would causes a disaster
#          }
#
#
##
class feature_downloader_hypervisor:

    def __init__(self, Nasdaq_code, start_date, feature_downloader_type_to_kw_lst_Map):

        self.Nasdaq_code = Nasdaq_code
        self.start_date = start_date
        self.feature_downloader_type_to_kw_lst_Map = feature_downloader_type_to_kw_lst_Map

        #the most import instance attribute
        self.feature_downloader_lst = []

        # This step instantiate all feature downloader Object for this stock
        for feature_downloader, keyword_lst in self.feature_downloader_type_to_kw_lst_Map.items():
            for kw in keyword_lst:
                self.feature_downloader_lst.append(feature_downloader(self.Nasdaq_code, kw, self.start_date))

    
    def describe(self):
        for one_feature_downloader in self.feature_downloader_lst:
            print(one_feature_downloader.describe())




feature_name_to_feature_downloader_Map = {
    "Nasdaq_code" : stock_price_downloader,
    "google_trend_kw_lst" : google_trend_downloader,
    "news_kw_lst" : google_news_downloader,
}




"Nasdaq_code", "start_date", "google_trend_kw_lst", "news_kw_lst"



####
#
# Purpose, as the name suggested 
# Each row in stock_and_features.csv represents eveything about one stock (its nasdaq_code, its features)
# Therefore it needs its own hypervisor 
#
####

def create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(one_row):
    feature_downloader_type_to_kw_lst_Map = {}

    Nasdaq_code = one_row["Nasdaq_code"]
    start_date = one_row["start_date"]
    google_trend_kw_lst = one_row["google_trend_kw_lst"].strip("[").strip("]").split(",")
    new_kw_lst = one_row["news_kw_lst"].strip("[").strip("]").split(",")

    feature_downloader_type_to_kw_lst_Map[feature_name_to_feature_downloader_Map["Nasdaq_code"]] = ["null"]
    feature_downloader_type_to_kw_lst_Map[feature_name_to_feature_downloader_Map["google_trend_kw_lst"]] = google_trend_kw_lst 
    feature_downloader_type_to_kw_lst_Map[feature_name_to_feature_downloader_Map["news_kw_lst"]] = new_kw_lst

    return feature_downloader_hypervisor(Nasdaq_code, start_date, feature_downloader_type_to_kw_lst_Map)

