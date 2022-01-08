

from Download.feature_downloader_hypervisor import create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv
import pandas as pd
import concurrent.futures
import random

#######
#
# This file is literally the soul of Download module, 
# it really puts all the APIs from utils
# and downloader objects together 
#
#######

stock_and_features_csv_path = "Data/stock_and_features.csv"
df = pd.read_csv(stock_and_features_csv_path)



#####
# 1 #
#   #
#####
def download_feature_from_web():
    #the following code will add all parallezable download process to the Lst
    #and use multi-processing to download them
    lst_of_download_raw_feature_processes = [ ]
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()
        #appending processes
        for downloader_object in i_th_row_stock_feature_downloader_lst:
            lst_of_download_raw_feature_processes += downloader_object.download_raw_feature_data_get_lst_of_process()

    ### actually starting to download them with multi-processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        print("There are " + str(len(lst_of_download_raw_feature_processes)) + " process needed to be run")
        random.shuffle(lst_of_download_raw_feature_processes)
        [executor.submit(proc) for proc in lst_of_download_raw_feature_processes]



#####
# 2 #
#   #
#####
def redownload_missing_feature_from_web():
    #the following code will add all parallezable download process to the Lst
    #and use multi-processing to download them
    lst_of_download_raw_feature_processes = [ ]
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()
        #appending processes
        for downloader_object in i_th_row_stock_feature_downloader_lst:
            lst_of_download_raw_feature_processes += downloader_object.redownload_missing_raw_feature_data_get_lst_of_process()

    ### actually starting to download them with multi-processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        print("There are " + str(len(lst_of_download_raw_feature_processes)) + " process needed to be run")
        random.shuffle(lst_of_download_raw_feature_processes)
        [executor.submit(proc) for proc in lst_of_download_raw_feature_processes]


#####
#2.5#
#   #
#####
def redownload_missing_feature_from_web_LAZY():
    #the following code will add all parallezable download process to the Lst
    #and use multi-processing to download them
    lst_of_download_raw_feature_processes = [ ]
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()
        #appending processes
        for downloader_object in i_th_row_stock_feature_downloader_lst:
            lst_of_download_raw_feature_processes += downloader_object.redownload_missing_raw_feature_data_get_lst_of_process_LAZY()

    ### actually starting to download them with multi-processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        print("There are " + str(len(lst_of_download_raw_feature_processes)) + " process needed to be run")
        random.shuffle(lst_of_download_raw_feature_processes)
        [executor.submit(proc) for proc in lst_of_download_raw_feature_processes]




#####
# 3 #
#   #
#####
def make_daily_report():
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_hypervisor.describe()
        i_th_row_stock_feature_downloader_hypervisor.write_overall_download_status_to_Data()



#####
# 4 #
#   #
#####
def check_missing_date_section():
    #the following code will add all parallezable download process to the Lst
    #and use multi-processing to download them
    lst_of_download_raw_feature_processes = [ ]
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()
        #appending processes

        for downloader_object in i_th_row_stock_feature_downloader_lst:
            print(downloader_object.NASDAQ_code + "    " + downloader_object.type_of_feature_downloader() + "    " + downloader_object.keyword)
            print(downloader_object.get_lst_of_missing_dates_time_sections())




#####
# 5 #
#   #
#####
def process_raw_feature():
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()

        for downloader_object in i_th_row_stock_feature_downloader_lst:
            downloader_object.process_raw_feature()



#####
# 6 #
#   #
#####
def dates_missing_corruption_recovery():
    for i in range(0, df.shape[0]):
        #initialize i_th_row
        i_th_row_stock = df.iloc[i]
        i_th_row_stock_feature_downloader_hypervisor = create_feature_downloader_hypervisor_from_one_row_of_stock_and_features_csv(i_th_row_stock)
        i_th_row_stock_feature_downloader_lst = i_th_row_stock_feature_downloader_hypervisor.get_feature_downloader_lst()

        for downloader_object in i_th_row_stock_feature_downloader_lst:
            downloader_object.dates_missing_data_corruption_recovery()




#download_feature_from_web()
redownload_missing_feature_from_web_LAZY()




process_raw_feature()
#make_daily_report()


#dates_missing_corruption_recovery()
check_missing_date_section()
print("DONE")