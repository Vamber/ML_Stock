
from Download.google_trend_downloader import google_trend_downloader
from Download.google_news_downloader import google_news_downloader
from Download.stock_price_downloader import stock_price_downloader
from os import path
import os
import csv 

from datetime import date 
import pandas as pd


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


feature_name_to_feature_downloader_Map = {
    "Nasdaq_code" : stock_price_downloader,
    "google_trend_kw_lst" : google_trend_downloader,
    "news_kw_lst" : google_news_downloader,
}

feature_downloader_type_to_df_column_name_Map = {
    "stock_price" : "stock_price",
    "google_news" : "news_kw_lst",
    "google_trend" : "google_trend_kw_lst",
}

df_daily_download_status = "Data/Daily_Download_Status/"

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

    def get_feature_downloader_lst(self):
        return self.feature_downloader_lst




    def write_overall_download_status_to_Data(self):

        
        columns  = ["Nasdaq_code"]
        columns.append(feature_downloader_type_to_df_column_name_Map["stock_price"])
        columns.append(feature_downloader_type_to_df_column_name_Map["google_news"])
        columns.append(feature_downloader_type_to_df_column_name_Map["google_trend"])
        #
        # ADD here if future feature need to be added
        #
        columns.append("download_verdict")
        columns.append("process_verdict")

        df_path_dir = df_daily_download_status
        df_path = df_path_dir  + "/" + str(date.today()) + ".csv"

        # Handling the case when Data/Daily_Download_Status/date.csv is not yet in the df

        if not path.exists(df_path_dir):
            os.makedirs(df_path_dir)

        if not path.exists(df_path):
            with open(df_path, mode = "w") as f:
                    f = csv.writer(f)
                    f.writerow(columns)

        
        # handling the case that the Nasdaq_code somehow already exist in df
        # although I don't know how earth it would happen, but if it happens, then we need to update it
        # therefore, deleteing that pre-existing row right now

        df = pd.read_csv(df_path)
        df = df[df.Nasdaq_code != self.Nasdaq_code]
        df.to_csv(df_path, index = False)




        ##
        ## Now, actually adding in stuffs
        ##

        new_row ={}
        google_news_status_Map = {}
        google_trend_status_Map = {}
        stock_price_status = 0
        download_verdict = 0
        process_verdict = 0

        #to save some string space, let's use some 1 for True 0 for False
        h = lambda status : 1 if status else 0 

        for feature_downloader in self.get_feature_downloader_lst():

            download_status = h(feature_downloader.is_download_successful_for_everyday())
            if feature_downloader.type_of_feature_downloader() == "stock_price":
                stock_price_status = download_status
            
            elif feature_downloader.type_of_feature_downloader() == "google_news":
                google_news_status_Map[feature_downloader.keyword] = download_status
            
            elif feature_downloader.type_of_feature_downloader() == "google_trend":
                google_trend_status_Map[feature_downloader.keyword] = download_status


        #f_d short for feature_downloader, otherwise the next long becomes too long
        download_verdict = all(   [f_d.is_download_successful_for_everyday() for f_d in self.get_feature_downloader_lst()]  )
        process_verdict = all( [f_d.is_processing_raw_feature_successful_for_everyday() for f_d in self.get_feature_downloader_lst()])
        #turn boolean into 1 and 0
        download_verdict = h(download_verdict)
        process_verdict = h(process_verdict)


        #initial the new row with value
        new_row["Nasdaq_code"] = self.Nasdaq_code
        new_row[feature_downloader_type_to_df_column_name_Map["stock_price"]] = stock_price_status
        new_row[feature_downloader_type_to_df_column_name_Map["google_news"]] = str(google_news_status_Map)
        new_row[feature_downloader_type_to_df_column_name_Map["google_trend"]] = str(google_trend_status_Map)

        new_row["download_verdict"] = download_verdict
        new_row["process_verdict"] = process_verdict


        # adding new row
        df = pd.read_csv(df_path)
        df = df.append(new_row, ignore_index=True)
        df.to_csv(df_path, index = False)


            
    







        

    
        



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

