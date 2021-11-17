
import os
# ensuring things are execute from the root of ML_stock
os.chdir("/home/vamber/ML_stock")

print(os.getcwd())

from Download.feature_downloader_hypervisor import create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv

import pandas as pd

#######
#
# This file is literally the soul of Download module, 
# it really puts all the APIs from utils
# and downloader objects together 
#
#######

stock_and_features_csv_path = "Data/stock_and_features.csv"

df = pd.read_csv(stock_and_features_csv_path)


for i in range(0, df.shape[0]):

    #initialize i_th_row
    i_th_row_stock = df.iloc[i]
    i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
    i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()

    #DOWNLOAD
    for downloader_object in i_th_row_stock_feature_downloader_lst:
        downloader_object.download_raw_feature_data()
        downloader_object.redownload_missing_raw_feature_data()


    #Send a report to user
    i_th_row_stock_feature_downloader_hypervisor.describe()
    i_th_row_stock_feature_downloader_hypervisor.write_overall_download_status_to_Data()

    

    