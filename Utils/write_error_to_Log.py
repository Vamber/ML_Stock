


##########################################
#
# This file creates the helper function that must be used by all functions downloading data from internent
#
# currently, those functions are:
# 1. get_all_news_metadata_from_a_keyword_on_a_particular_date(stock_NASDAQ_code, keyword, date)
# 2. get_the_number_of_news_published_pertaining_to_the_keyword(stock_NASDAQ_code, keyword, date)
# 3. 
#
#

# It will create a file called 2021/08/05.txt and store it into the Data/Log/Error directory 
#
#
#########################################


import csv

import datetime as DT


from os import path
import os

def write_download_error_msg_to_Log(date, stock_NASDAQ_code, function_name, function_args):

	today = str(DT.date.today())
	
	
	Path = "/home/vamber/ML_stock/Data/Log/Download_Error/"
	
	file_name = Path + stock_NASDAQ_code + ".csv"

	#this if clause just write the header for the file that's about to be created
	if not path.exists(file_name):

		with open(file_name, mode = "w") as f:
			f = csv.writer(f)
			f.writerow(["date", "stock_name", "function_name", "function_args"])
		
	#actual content of the msg is actually written by this following clause
	#Per design doc, each row correspond to to an incident of download error

	#like this:    2021-03-25,  TSLA,   get_all_news_metadata_from_a_particular_date,  Tesla_stock
	with open(file_name, mode = "a") as f:
		f = csv.writer(f)
		f.writerow([date, stock_NASDAQ_code, function_name, function_args])



	
